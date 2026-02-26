"""
Extra schemas - Notes, Calendar, Sharing, Comments, Templates
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# ===========================================
# Notes
# ===========================================

class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    content: str
    note_type: Optional[str] = "general"
    tags: List[str] = []
    is_pinned: bool = False


class NoteCreate(NoteBase):
    meeting_id: UUID


class NoteResponse(NoteBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    meeting_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


# ===========================================
# Calendar
# ===========================================

class CalendarEventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    meeting_link: Optional[str] = None


class CalendarEventResponse(CalendarEventBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    external_id: Optional[str] = None
    attendees: List[dict] = []
    provider: Optional[str] = None
    is_meetingmind_meeting: bool = False
    meeting_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime


class CalendarSyncRequest(BaseModel):
    provider: str  # google, outlook, apple


# ===========================================
# Sharing
# ===========================================

class MeetingShareBase(BaseModel):
    shared_with_email: str
    permission_level: str = "view"
    message: Optional[str] = None
    expires_at: Optional[datetime] = None


class MeetingShareCreate(MeetingShareBase):
    pass


class MeetingShareResponse(MeetingShareBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    meeting_id: UUID
    owner_user_id: UUID
    is_accepted: bool = False
    created_at: datetime


# ===========================================
# Comments
# ===========================================

class CommentBase(BaseModel):
    content: str
    parent_id: Optional[UUID] = None
    transcript_id: Optional[UUID] = None


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    meeting_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


# ===========================================
# AI Templates
# ===========================================

class AITemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    template_type: str = "summary"
    prompt_template: str
    output_format: dict = {}


class AITemplateCreate(AITemplateBase):
    pass


class AITemplateResponse(AITemplateBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    organization_id: Optional[UUID] = None
    is_default: bool = False
    created_at: datetime
    updated_at: datetime
