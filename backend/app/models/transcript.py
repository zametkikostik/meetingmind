"""
Transcript, Action Item, and Knowledge Graph models
"""
from sqlalchemy import (
    Column, String, Boolean, Integer, DateTime, Date,
    ForeignKey, Text, Enum as SQLEnum, DECIMAL, func, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import JSON
import uuid
from enum import Enum

from .base import Base, TimestampMixin


class ActionItemStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Transcript(Base):
    """Transcript segment model"""
    
    __tablename__ = "transcripts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meeting_id = Column(
        UUID(as_uuid=True),
        ForeignKey("meetings.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    participant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("meeting_participants.id", ondelete="SET NULL"),
        index=True
    )
    speaker_name = Column(String(255))
    text = Column(Text, nullable=False)
    start_time = Column(DECIMAL(10, 3), nullable=False)
    end_time = Column(DECIMAL(10, 3), nullable=False)
    confidence = Column(DECIMAL(3, 2))
    sentiment = Column(String(20))
    is_key_moment = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    
    # Relationships
    meeting = relationship("Meeting", back_populates="transcripts")
    participant = relationship("MeetingParticipant", back_populates="transcripts")
    
    def __repr__(self) -> str:
        return f"<Transcript(id={self.id}, start={self.start_time}s)>"


class ActionItem(Base, TimestampMixin):
    """Action item model"""
    
    __tablename__ = "action_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meeting_id = Column(
        UUID(as_uuid=True),
        ForeignKey("meetings.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    assignee_user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True
    )
    assignee_name = Column(String(255))
    assignee_email = Column(String(255))
    task = Column(Text, nullable=False)
    status = Column(
        SQLEnum(ActionItemStatus),
        default=ActionItemStatus.PENDING,
        index=True
    )
    priority = Column(String(20), default="medium")
    due_date = Column(Date)
    completed_at = Column(DateTime(timezone=True))
    transcript_id = Column(
        UUID(as_uuid=True),
        ForeignKey("transcripts.id")
    )

    # Relationships
    meeting = relationship("Meeting", back_populates="action_items")
    assignee = relationship("User", back_populates="action_items")
    transcript = relationship("Transcript", backref="action_items")

    def __repr__(self) -> str:
        return f"<ActionItem(id={self.id}, task={self.task[:30]}...)>"


class KnowledgeNode(Base):
    """Knowledge graph node model"""
    
    __tablename__ = "knowledge_nodes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name = Column(String(255), nullable=False)
    node_type = Column(String(50), nullable=False, index=True)
    description = Column(Text)
    node_metadata = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=func.now())
    
    # Relationships
    organization = relationship("Organization", back_populates="knowledge_nodes")
    outgoing_edges = relationship(
        "KnowledgeEdge",
        foreign_keys="KnowledgeEdge.source_node_id",
        back_populates="source_node"
    )
    incoming_edges = relationship(
        "KnowledgeEdge",
        foreign_keys="KnowledgeEdge.target_node_id",
        back_populates="target_node"
    )
    
    __table_args__ = (
        UniqueConstraint("organization_id", "name", "node_type", name="uq_knowledge_node"),
    )
    
    def __repr__(self) -> str:
        return f"<KnowledgeNode(name={self.name}, type={self.node_type})>"


class KnowledgeEdge(Base):
    """Knowledge graph edge model"""
    
    __tablename__ = "knowledge_edges"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_node_id = Column(
        UUID(as_uuid=True),
        ForeignKey("knowledge_nodes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    target_node_id = Column(
        UUID(as_uuid=True),
        ForeignKey("knowledge_nodes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    edge_type = Column(String(50), nullable=False)
    strength = Column(DECIMAL(3, 2), default=1.0)
    meeting_id = Column(
        UUID(as_uuid=True),
        ForeignKey("meetings.id", ondelete="SET NULL")
    )
    created_at = Column(DateTime(timezone=True), default=func.now())
    
    # Relationships
    source_node = relationship(
        "KnowledgeNode",
        foreign_keys=[source_node_id],
        back_populates="outgoing_edges"
    )
    target_node = relationship(
        "KnowledgeNode",
        foreign_keys=[target_node_id],
        back_populates="incoming_edges"
    )
    meeting = relationship("Meeting")
    
    __table_args__ = (
        UniqueConstraint("source_node_id", "target_node_id", "edge_type", name="uq_knowledge_edge"),
    )
    
    def __repr__(self) -> str:
        return f"<KnowledgeEdge({self.edge_type}: {self.source_node_id} -> {self.target_node_id})>"
