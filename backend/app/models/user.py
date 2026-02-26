"""
User model
"""
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime

from .base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """User model"""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    avatar_url = Column(String)
    timezone = Column(String(50), default="UTC")
    language = Column(String(10), default="en")
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Relationships
    meetings = relationship("MeetingParticipant", back_populates="user")
    action_items = relationship("ActionItem", back_populates="assignee")
    refresh_tokens = relationship("RefreshToken", back_populates="user")
    organization_memberships = relationship(
        "OrganizationMember",
        back_populates="user"
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
