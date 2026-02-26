"""
Notes, Calendar, and Sharing API endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timedelta

from ..db.session import get_db
from ..models.user import User
from ..models.meeting import Meeting
from ..models.extra import Note, CalendarEvent, MeetingShare, Comment, AITemplate
from ..schemas.extra import (
    NoteCreate,
    NoteResponse,
    CalendarEventResponse,
    MeetingShareCreate,
    MeetingShareResponse,
    CommentCreate,
    CommentResponse,
    AITemplateCreate,
    AITemplateResponse,
)
from ..core.deps import get_current_user

router = APIRouter(prefix="/extras", tags=["Notes", "Calendar", "Sharing"])


# ===========================================
# Notes Endpoints
# ===========================================

@router.get("/notes", response_model=List[NoteResponse])
def list_notes(
    meeting_id: Optional[UUID] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List notes"""
    query = db.query(Note).filter(Note.user_id == current_user.id)
    
    if meeting_id:
        query = query.filter(Note.meeting_id == meeting_id)
    
    notes = query.order_by(Note.is_pinned.desc(), Note.created_at.desc()).offset(skip).limit(limit).all()
    return notes


@router.post("/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    note_data: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new note"""
    note = Note(
        user_id=current_user.id,
        **note_data.model_dump()
    )
    
    db.add(note)
    db.commit()
    db.refresh(note)
    
    return note


@router.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: UUID,
    note_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update note"""
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    for field, value in note_data.items():
        setattr(note, field, value)
    
    db.commit()
    db.refresh(note)
    return note


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete note"""
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(note)
    db.commit()


# ===========================================
# Calendar Endpoints
# ===========================================

@router.get("/calendar/events", response_model=List[CalendarEventResponse])
def list_calendar_events(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List calendar events"""
    query = db.query(CalendarEvent).filter(CalendarEvent.user_id == current_user.id)
    
    if start_date:
        query = query.filter(CalendarEvent.start_time >= start_date)
    if end_date:
        query = query.filter(CalendarEvent.start_time <= end_date)
    
    events = query.order_by(CalendarEvent.start_time).all()
    return events


@router.post("/calendar/sync", response_model=dict)
def sync_calendar(
    provider: str = Query(...),  # google, outlook
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Sync calendar events from provider
    
    Note: This requires OAuth flow implementation
    """
    # Check if integration exists
    from ..models.extra import CalendarIntegration
    
    integration = db.query(CalendarIntegration).filter(
        CalendarIntegration.user_id == current_user.id,
        CalendarIntegration.provider == provider
    ).first()
    
    if not integration:
        raise HTTPException(
            status_code=400,
            detail=f"Calendar integration with {provider} not found. Please connect first."
        )
    
    # TODO: Implement actual calendar sync
    # This would call Google Calendar API or Microsoft Graph API
    
    return {"status": "synced", "provider": provider}


# ===========================================
# Sharing Endpoints
# ===========================================

@router.post("/meetings/{meeting_id}/share", response_model=MeetingShareResponse)
def share_meeting(
    meeting_id: UUID,
    share_data: MeetingShareCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Share meeting with someone"""
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    share = MeetingShare(
        meeting_id=meeting_id,
        owner_user_id=current_user.id,
        **share_data.model_dump()
    )
    
    db.add(share)
    db.commit()
    db.refresh(share)
    
    # TODO: Send email notification
    
    return share


@router.get("/meetings/{meeting_id}/shares", response_model=List[MeetingShareResponse])
def list_meeting_shares(
    meeting_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all shares for a meeting"""
    shares = db.query(MeetingShare).filter(
        MeetingShare.meeting_id == meeting_id,
        MeetingShare.owner_user_id == current_user.id
    ).all()
    
    return shares


# ===========================================
# Comments Endpoints
# ===========================================

@router.get("/meetings/{meeting_id}/comments", response_model=List[CommentResponse])
def list_comments(
    meeting_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List comments for a meeting"""
    comments = db.query(Comment).filter(
        Comment.meeting_id == meeting_id
    ).order_by(Comment.created_at).all()
    
    return comments


@router.post("/meetings/{meeting_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    meeting_id: UUID,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a comment on a meeting"""
    comment = Comment(
        meeting_id=meeting_id,
        user_id=current_user.id,
        **comment_data.model_dump()
    )
    
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    return comment


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a comment"""
    comment = db.query(Comment).filter(
        Comment.id == comment_id,
        Comment.user_id == current_user.id
    ).first()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    db.delete(comment)
    db.commit()


# ===========================================
# AI Templates Endpoints
# ===========================================

@router.get("/templates", response_model=List[AITemplateResponse])
def list_templates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List AI templates"""
    templates = db.query(AITemplate).filter(
        AITemplate.user_id == current_user.id
    ).all()
    
    return templates


@router.post("/templates", response_model=AITemplateResponse, status_code=status.HTTP_201_CREATED)
def create_template(
    template_data: AITemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a custom AI template"""
    template = AITemplate(
        user_id=current_user.id,
        **template_data.model_dump()
    )
    
    db.add(template)
    db.commit()
    db.refresh(template)
    
    return template


@router.delete("/templates/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(
    template_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a template"""
    template = db.query(AITemplate).filter(
        AITemplate.id == template_id,
        AITemplate.user_id == current_user.id
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    db.delete(template)
    db.commit()
