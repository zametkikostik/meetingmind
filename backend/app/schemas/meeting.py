"""
Meeting schemas
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID
from enum import Enum


class MeetingStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ParticipantRole(str, Enum):
    HOST = "host"
    PARTICIPANT = "participant"
    GUEST = "guest"


# Meeting Participant
class MeetingParticipantBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: ParticipantRole = ParticipantRole.PARTICIPANT


class MeetingParticipantCreate(MeetingParticipantBase):
    meeting_id: UUID


class MeetingParticipantResponse(MeetingParticipantBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    meeting_id: UUID
    user_id: Optional[UUID] = None
    join_time: Optional[datetime] = None
    leave_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    talk_time_seconds: int = 0
    is_speaker: bool = False


# Transcript segment
class TranscriptBase(BaseModel):
    text: str
    speaker_name: Optional[str] = None
    start_time: float
    end_time: float


class TranscriptCreate(TranscriptBase):
    meeting_id: UUID
    participant_id: Optional[UUID] = None


class TranscriptResponse(TranscriptBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    meeting_id: UUID
    participant_id: Optional[UUID] = None
    confidence: Optional[float] = None
    sentiment: Optional[str] = None
    is_key_moment: bool = False
    created_at: datetime


# Action Item
class ActionItemStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ActionItemBase(BaseModel):
    task: str
    assignee_name: Optional[str] = None
    assignee_email: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[date] = None


class ActionItemCreate(ActionItemBase):
    meeting_id: UUID


class ActionItemUpdate(BaseModel):
    task: Optional[str] = None
    status: Optional[ActionItemStatus] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None


class ActionItemResponse(ActionItemBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    meeting_id: UUID
    assignee_user_id: Optional[UUID] = None
    status: ActionItemStatus
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


# Meeting
class MeetingBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    platform: Optional[str] = None
    scheduled_at: Optional[datetime] = None


class MeetingCreate(MeetingBase):
    organization_id: Optional[UUID] = None


class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[MeetingStatus] = None
    summary: Optional[str] = None


class MeetingResponse(MeetingBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    organization_id: UUID
    external_id: Optional[str] = None
    status: MeetingStatus
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    recording_url: Optional[str] = None
    transcript_status: str
    analysis_status: str
    summary: Optional[str] = None
    key_topics: List[str] = []
    sentiment_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime


# Meeting with relationships
class MeetingDetailResponse(MeetingResponse):
    participants: List[MeetingParticipantResponse] = []
    transcripts: List[TranscriptResponse] = []
    action_items: List[ActionItemResponse] = []


# Knowledge Graph
class KnowledgeNodeBase(BaseModel):
    name: str
    node_type: str
    description: Optional[str] = None
    metadata: dict = {}


class KnowledgeNodeCreate(KnowledgeNodeBase):
    organization_id: UUID


class KnowledgeNodeResponse(KnowledgeNodeBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    organization_id: UUID
    created_at: datetime


class KnowledgeEdgeBase(BaseModel):
    edge_type: str
    strength: float = 1.0


class KnowledgeEdgeCreate(KnowledgeEdgeBase):
    source_node_id: UUID
    target_node_id: UUID
    meeting_id: Optional[UUID] = None


class KnowledgeEdgeResponse(KnowledgeEdgeBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    source_node_id: UUID
    target_node_id: UUID
    meeting_id: Optional[UUID] = None
    created_at: datetime
