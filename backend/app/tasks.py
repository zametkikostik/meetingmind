"""
Celery tasks for AI processing
"""
import os
import sys
import tempfile
from datetime import datetime

# Add ai-engine to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "ai-engine"))

from app.celery import celery_app
from app.db.session import SessionLocal
from app.models.meeting import Meeting, MeetingStatus
from app.models.transcript import Transcript, ActionItem, ActionItemStatus


@celery_app.task(bind=True, max_retries=3)
def transcribe_meeting(self, meeting_id: str):
    """
    Transcribe meeting audio using Whisper
    
    Args:
        meeting_id: UUID of the meeting
    """
    from ai_engine.transcription import WhisperTranscriber, TranscriberConfig
    
    db = SessionLocal()
    
    try:
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        
        if not meeting:
            raise ValueError(f"Meeting {meeting_id} not found")
        
        # Update status
        meeting.transcript_status = "processing"
        db.commit()
        
        # Download recording
        recording_path = download_recording(meeting.recording_url)
        
        # Create transcriber
        config = TranscriberConfig(
            model=os.environ.get("WHISPER_MODEL", "base"),
            use_local=os.environ.get("USE_LOCAL_WHISPER", "false").lower() == "true",
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
        )
        
        transcriber = WhisperTranscriber(config)
        
        # Transcribe with progress callback
        segments = transcriber.transcribe_file(
            recording_path,
            progress_callback=lambda data: update_transcription_progress(
                meeting_id, data, db
            )
        )
        
        # Save transcripts to database
        for segment in segments:
            transcript = Transcript(
                meeting_id=meeting_id,
                text=segment.text,
                start_time=segment.start,
                end_time=segment.end,
                speaker_name=segment.speaker or "Unknown",
                confidence=segment.confidence,
            )
            db.add(transcript)
        
        # Update meeting status
        meeting.transcript_status = "completed"
        db.commit()
        
        # Trigger analysis task
        analyze_meeting.delay(meeting_id)
        
        return {"status": "completed", "segments_count": len(segments)}
        
    except Exception as e:
        meeting.transcript_status = "failed"
        db.commit()
        raise self.retry(exc=e, countdown=60)
        
    finally:
        db.close()
        # Cleanup temp file
        if "recording_path" in locals() and os.path.exists(recording_path):
            os.unlink(recording_path)


@celery_app.task(bind=True, max_retries=3)
def analyze_meeting(self, meeting_id: str):
    """
    Analyze meeting transcript using LLM
    
    Args:
        meeting_id: UUID of the meeting
    """
    from ai_engine.analysis import MeetingAnalyzer
    
    db = SessionLocal()
    
    try:
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        
        if not meeting:
            raise ValueError(f"Meeting {meeting_id} not found")
        
        # Update status
        meeting.analysis_status = "processing"
        db.commit()
        
        # Load transcripts
        transcripts = (
            db.query(Transcript)
            .filter(Transcript.meeting_id == meeting_id)
            .order_by(Transcript.start_time)
            .all()
        )
        
        # Format for analyzer
        transcript_data = [
            {
                "speaker": t.speaker_name,
                "text": t.text,
                "start": float(t.start_time),
                "end": float(t.end_time),
            }
            for t in transcripts
        ]
        
        # Get previous meetings for context
        previous_meetings = get_previous_meeting_summaries(db, meeting)
        
        # Create analyzer
        analyzer = MeetingAnalyzer(
            llm_provider=os.environ.get("LLM_PROVIDER", "openai"),
            api_key=os.environ.get("LLM_API_KEY"),
            model=os.environ.get("LLM_MODEL", "gpt-4o-mini"),
        )
        
        # Analyze
        result = analyzer.analyze_meeting(
            transcript=transcript_data,
            meeting_title=meeting.title,
            previous_meetings=previous_meetings,
        )
        
        # Save results
        meeting.summary = result.summary
        meeting.key_topics = result.key_topics
        meeting.sentiment_score = result.sentiment_score
        meeting.analysis_status = "completed"
        
        # Mark key moments in transcripts
        for moment in result.key_moments:
            # Find closest transcript segment
            # (simplified - in production would match by timestamp)
            pass
        
        # Create action items
        for item in result.action_items:
            action_item = ActionItem(
                meeting_id=meeting_id,
                task=item.get("task", ""),
                assignee_name=item.get("assignee"),
                priority=item.get("priority", "medium"),
                status=ActionItemStatus.PENDING,
            )
            db.add(action_item)
        
        db.commit()
        
        # Update knowledge graph
        if os.environ.get("ENABLE_KNOWLEDGE_GRAPH", "true").lower() == "true":
            update_knowledge_graph.delay(meeting_id, result.knowledge_graph_updates)
        
        return {"status": "completed", "summary_length": len(result.summary)}
        
    except Exception as e:
        meeting.analysis_status = "failed"
        db.commit()
        raise self.retry(exc=e, countdown=60)
        
    finally:
        db.close()


@celery_app.task
def update_knowledge_graph(meeting_id: str, updates: dict):
    """
    Update knowledge graph with new entities and relationships
    
    Args:
        meeting_id: UUID of the meeting
        updates: Knowledge graph updates from analysis
    """
    from app.models.transcript import KnowledgeNode, KnowledgeEdge
    
    db = SessionLocal()
    
    try:
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        
        if not meeting:
            return
        
        # Add new entities
        for entity in updates.get("entities", []):
            node = KnowledgeNode(
                organization_id=meeting.organization_id,
                name=entity["name"],
                node_type=entity["type"],
                description=entity.get("description"),
                metadata=entity.get("metadata", {}),
            )
            db.merge(node)  # Use merge to avoid duplicates
        
        # Add relationships
        for rel in updates.get("relationships", []):
            edge = KnowledgeEdge(
                source_node_id=rel["source"],
                target_node_id=rel["target"],
                edge_type=rel["type"],
                strength=rel.get("strength", 1.0),
                meeting_id=meeting_id,
            )
            db.add(edge)
        
        db.commit()
        
    except Exception as e:
        db.rollback()
        print(f"Knowledge graph update error: {e}")
        
    finally:
        db.close()


def download_recording(url: str) -> str:
    """Download recording from S3 or URL"""
    import boto3
    from urllib.parse import urlparse
    
    # Check if S3 URL
    if "s3" in url or urlparse(url).netloc:
        # Download from S3
        s3_client = boto3.client(
            "s3",
            endpoint_url=os.environ.get("S3_ENDPOINT_URL"),
            aws_access_key_id=os.environ.get("S3_ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("S3_SECRET_KEY"),
        )
        
        # Parse bucket and key
        # Format: s3://bucket/key or http://minio:9000/bucket/key
        if "s3://" in url:
            parts = url.replace("s3://", "").split("/")
            bucket = parts[0]
            key = "/".join(parts[1:])
        else:
            parts = urlparse(url).path.strip("/").split("/")
            bucket = parts[0]
            key = "/".join(parts[1:])
        
        # Download to temp file
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        s3_client.download_file(bucket, key, temp_file.name)
        temp_file.close()
        
        return temp_file.name
    
    # Regular URL download
    import httpx
    
    temp_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    
    with httpx.stream("GET", url, follow_redirects=True) as response:
        response.raise_for_status()
        for chunk in response.iter_bytes():
            temp_file.write(chunk)
    
    temp_file.close()
    return temp_file.name


def update_transcription_progress(meeting_id: str, data: dict, db):
    """Update transcription progress (for WebSocket updates)"""
    # This would send progress via WebSocket in production
    pass


def get_previous_meeting_summaries(db, meeting) -> list:
    """Get summaries of previous meetings for context"""
    previous = (
        db.query(Meeting)
        .filter(
            Meeting.organization_id == meeting.organization_id,
            Meeting.id != meeting.id,
            Meeting.status == MeetingStatus.COMPLETED,
        )
        .order_by(Meeting.created_at.desc())
        .limit(3)
        .all()
    )
    
    return [m.summary for m in previous if m.summary]
