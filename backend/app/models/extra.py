"""
Notes, Calendar, and Sharing models
"""
from sqlalchemy import (
    Column, String, Boolean, Integer, DateTime, Date, Text,
    ForeignKey, Enum as SQLEnum, DECIMAL
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import JSON
import uuid
from enum import Enum

from .base import Base, TimestampMixin
from sqlalchemy import func, UniqueConstraint


class Note(Base, TimestampMixin):
    """Manual meeting notes model"""
    
    __tablename__ = "notes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meeting_id = Column(
        UUID(as_uuid=True),
        ForeignKey("meetings.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    note_type = Column(String(50), default="general")
    tags = Column(JSON, default=list)
    is_pinned = Column(Boolean, default=False)
    
    # Relationships
    meeting = relationship("Meeting", back_populates="notes")
    user = relationship("User")
    
    def __repr__(self) -> str:
        return f"<Note(id={self.id}, title={self.title[:30]}...)>"


class CalendarIntegration(Base):
    """Calendar integration model (Google, Outlook)"""
    
    __tablename__ = "calendar_integrations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    provider = Column(String(50), nullable=False)  # google, outlook, apple
    provider_user_id = Column(String(255))
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text)
    token_expires_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    last_synced_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=func.now())
    
    # Relationships
    user = relationship("User")
    
    __table_args__ = (
        UniqueConstraint("user_id", "provider", name="uq_calendar_integration"),
    )
    
    def __repr__(self) -> str:
        return f"<CalendarIntegration(user={self.user_id}, provider={self.provider})>"


class CalendarEvent(Base, TimestampMixin):
    """Calendar event model"""
    
    __tablename__ = "calendar_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    external_id = Column(String(255), index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    end_time = Column(DateTime(timezone=True), nullable=False)
    meeting_link = Column(Text)
    attendees = Column(JSON, default=list)
    provider = Column(String(50))
    is_meetingmind_meeting = Column(Boolean, default=False)
    meeting_id = Column(
        UUID(as_uuid=True),
        ForeignKey("meetings.id", ondelete="SET NULL")
    )
    
    # Relationships
    user = relationship("User")
    meeting = relationship("Meeting")
    
    def __repr__(self) -> str:
        return f"<CalendarEvent(title={self.title}, start={self.start_time})>"


class MeetingShare(Base):
    """Meeting sharing model"""
    
    __tablename__ = "meeting_shares"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meeting_id = Column(
        UUID(as_uuid=True),
        ForeignKey("meetings.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    owner_user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    shared_with_email = Column(String(255), nullable=False, index=True)
    permission_level = Column(String(50), default="view")  # view, edit, admin
    message = Column(Text)
    expires_at = Column(DateTime(timezone=True))
    is_accepted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    
    # Relationships
    meeting = relationship("Meeting")
    owner = relationship("User", foreign_keys=[owner_user_id])
    
    __table_args__ = (
        UniqueConstraint("meeting_id", "shared_with_email", name="uq_meeting_share"),
    )
    
    def __repr__(self) -> str:
        return f"<MeetingShare(meeting={self.meeting_id}, email={self.shared_with_email})>"


class Comment(Base, TimestampMixin):
    """Comment model for meetings and transcripts"""
    
    __tablename__ = "comments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meeting_id = Column(
        UUID(as_uuid=True),
        ForeignKey("meetings.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    parent_id = Column(
        UUID(as_uuid=True),
        ForeignKey("comments.id", ondelete="CASCADE"),
        index=True
    )
    transcript_id = Column(
        UUID(as_uuid=True),
        ForeignKey("transcripts.id", ondelete="CASCADE"),
        index=True
    )
    content = Column(Text, nullable=False)
    
    # Relationships
    meeting = relationship("Meeting", back_populates="comments")
    user = relationship("User")
    parent = relationship("Comment", remote_side=[id])
    transcript = relationship("Transcript")
    replies = relationship("Comment", remote_side=[parent_id])
    
    def __repr__(self) -> str:
        return f"<Comment(id={self.id}, meeting={self.meeting_id})>"


class AITemplate(Base, TimestampMixin):
    """AI template for custom summaries and analysis"""
    
    __tablename__ = "ai_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        index=True
    )
    name = Column(String(255), nullable=False)
    description = Column(Text)
    template_type = Column(String(50), default="summary")
    prompt_template = Column(Text, nullable=False)
    output_format = Column(JSON, default=dict)
    is_default = Column(Boolean, default=False)
    
    def __repr__(self) -> str:
        return f"<AITemplate(name={self.name}, type={self.template_type})>"


# Add back-references to existing models
from .meeting import Meeting
from .transcript import Transcript

Meeting.notes = relationship("Note", back_populates="meeting", cascade="all, delete-orphan")
Meeting.comments = relationship("Comment", back_populates="meeting", cascade="all, delete-orphan")
Transcript.comments = relationship("Comment", back_populates="transcript", cascade="all, delete-orphan")
