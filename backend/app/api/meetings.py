"""
Meetings API endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID

from ..db.session import get_db
from ..models.user import User
from ..models.meeting import Meeting, MeetingParticipant, MeetingStatus
from ..schemas.meeting import (
    MeetingCreate,
    MeetingUpdate,
    MeetingResponse,
    MeetingDetailResponse,
    MeetingParticipantCreate,
    MeetingParticipantResponse,
    ActionItemCreate,
    ActionItemUpdate,
    ActionItemResponse,
    TranscriptResponse,
)
from ..core.deps import get_current_user

router = APIRouter(prefix="/meetings", tags=["Meetings"])


@router.get("", response_model=List[MeetingResponse])
def list_meetings(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[MeetingStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all meetings for current user
    """
    query = db.query(Meeting)
    
    if status_filter:
        query = query.filter(Meeting.status == status_filter)
    
    meetings = query.order_by(Meeting.created_at.desc()).offset(skip).limit(limit).all()
    
    return meetings


@router.post("", response_model=MeetingResponse, status_code=status.HTTP_201_CREATED)
def create_meeting(
    meeting_data: MeetingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new meeting
    """
    meeting = Meeting(
        **meeting_data.model_dump(),
    )
    
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    
    return meeting


@router.get("/{meeting_id}", response_model=MeetingDetailResponse)
def get_meeting(
    meeting_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get meeting details
    """
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    
    return meeting


@router.put("/{meeting_id}", response_model=MeetingResponse)
def update_meeting(
    meeting_id: UUID,
    meeting_data: MeetingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update meeting
    """
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    
    update_data = meeting_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(meeting, field, value)
    
    db.commit()
    db.refresh(meeting)
    
    return meeting


@router.delete("/{meeting_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meeting(
    meeting_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete meeting
    """
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    
    db.delete(meeting)
    db.commit()
    
    return None


@router.post("/{meeting_id}/participants", response_model=MeetingParticipantResponse)
def add_participant(
    meeting_id: UUID,
    participant_data: MeetingParticipantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Add participant to meeting
    """
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    
    participant = MeetingParticipant(
        meeting_id=meeting_id,
        **participant_data.model_dump(exclude={"meeting_id"})
    )
    
    db.add(participant)
    db.commit()
    db.refresh(participant)
    
    return participant


@router.get("/{meeting_id}/transcripts", response_model=List[TranscriptResponse])
def get_transcripts(
    meeting_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get meeting transcripts
    """
    from ..models.transcript import Transcript
    
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    
    transcripts = db.query(Transcript).filter(
        Transcript.meeting_id == meeting_id
    ).order_by(Transcript.start_time).all()
    
    return transcripts


@router.post("/{meeting_id}/action-items", response_model=ActionItemResponse, status_code=status.HTTP_201_CREATED)
def create_action_item(
    meeting_id: UUID,
    action_data: ActionItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create action item for meeting
    """
    from ..models.transcript import ActionItem, ActionItemStatus
    
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found"
        )
    
    action_item = ActionItem(
        meeting_id=meeting_id,
        **action_data.model_dump(exclude={"meeting_id"})
    )
    
    db.add(action_item)
    db.commit()
    db.refresh(action_item)
    
    return action_item


@router.put("/action-items/{action_id}", response_model=ActionItemResponse)
def update_action_item(
    action_id: UUID,
    action_data: ActionItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update action item
    """
    from ..models.transcript import ActionItem
    
    action_item = db.query(ActionItem).filter(ActionItem.id == action_id).first()
    
    if not action_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Action item not found"
        )
    
    update_data = action_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(action_item, field, value)
    
    db.commit()
    db.refresh(action_item)
    
    return action_item
