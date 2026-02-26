"""
Organization and Meeting models
"""
from sqlalchemy import (
    Column, String, Boolean, Integer, DateTime,
    ForeignKey, Text, Enum as SQLEnum, DECIMAL, func, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import JSON
import uuid
from enum import Enum

from .base import Base, TimestampMixin


class MeetingStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ParticipantRole(str, Enum):
    HOST = "host"
    PARTICIPANT = "participant"
    GUEST = "guest"


class Organization(Base, TimestampMixin):
    """Organization (Team) model"""
    
    __tablename__ = "organizations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    logo_url = Column(String)
    plan_type = Column(String(50), default="free")
    max_meetings = Column(Integer, default=100)
    max_storage_gb = Column(Integer, default=10)
    
    # Relationships
    members = relationship("OrganizationMember", back_populates="organization")
    meetings = relationship("Meeting", back_populates="organization")
    knowledge_nodes = relationship("KnowledgeNode", back_populates="organization")
    
    def __repr__(self) -> str:
        return f"<Organization(id={self.id}, slug={self.slug})>"


class OrganizationMember(Base):
    """Organization member model"""
    
    __tablename__ = "organization_members"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    role = Column(String(50), default="member")
    joined_at = Column(DateTime(timezone=True), default=func.now())
    
    # Relationships
    organization = relationship("Organization", back_populates="members")
    user = relationship("User", back_populates="organization_memberships")
    
    __table_args__ = (
        UniqueConstraint("organization_id", "user_id", name="uq_org_member"),
    )
    
    def __repr__(self) -> str:
        return f"<OrganizationMember(org={self.organization_id}, user={self.user_id})>"


class Meeting(Base, TimestampMixin):
    """Meeting model"""
    
    __tablename__ = "meetings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False
    )
    title = Column(String(500), nullable=False)
    description = Column(Text)
    external_id = Column(String(255))
    platform = Column(String(50))
    status = Column(
        SQLEnum(MeetingStatus),
        default=MeetingStatus.SCHEDULED,
        index=True
    )
    scheduled_at = Column(DateTime(timezone=True), index=True)
    started_at = Column(DateTime(timezone=True))
    ended_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Integer)
    recording_url = Column(String)
    transcript_status = Column(String(50), default="pending")
    analysis_status = Column(String(50), default="pending")
    summary = Column(Text)
    key_topics = Column(JSON, default=list)
    sentiment_score = Column(DECIMAL(3, 2))
    
    # Relationships
    organization = relationship("Organization", back_populates="meetings")
    participants = relationship(
        "MeetingParticipant",
        back_populates="meeting",
        cascade="all, delete-orphan"
    )
    transcripts = relationship(
        "Transcript",
        back_populates="meeting",
        cascade="all, delete-orphan"
    )
    action_items = relationship(
        "ActionItem",
        back_populates="meeting",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Meeting(id={self.id}, title={self.title[:30]}...)>"


class MeetingParticipant(Base):
    """Meeting participant model"""
    
    __tablename__ = "meeting_participants"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meeting_id = Column(
        UUID(as_uuid=True),
        ForeignKey("meetings.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True
    )
    email = Column(String(255))
    name = Column(String(255))
    role = Column(SQLEnum(ParticipantRole), default=ParticipantRole.PARTICIPANT)
    join_time = Column(DateTime(timezone=True))
    leave_time = Column(DateTime(timezone=True))
    duration_seconds = Column(Integer)
    talk_time_seconds = Column(Integer, default=0)
    is_speaker = Column(Boolean, default=False)
    
    # Relationships
    meeting = relationship("Meeting", back_populates="participants")
    user = relationship("User", back_populates="meetings")
    transcripts = relationship("Transcript", back_populates="participant")
    
    def __repr__(self) -> str:
        return f"<MeetingParticipant(meeting={self.meeting_id}, name={self.name})>"
