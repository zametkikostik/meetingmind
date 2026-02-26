"""
Models module
"""
from .base import Base, TimestampMixin
from .user import User
from .meeting import (
    Organization,
    OrganizationMember,
    Meeting,
    MeetingParticipant,
    MeetingStatus,
    ParticipantRole,
)
from .transcript import (
    Transcript,
    ActionItem,
    ActionItemStatus,
    KnowledgeNode,
    KnowledgeEdge,
)
from .token import RefreshToken
from .extra import (
    Note,
    CalendarIntegration,
    CalendarEvent,
    MeetingShare,
    Comment,
    AITemplate,
)


__all__ = [
    "Base",
    "TimestampMixin",
    "User",
    "Organization",
    "OrganizationMember",
    "Meeting",
    "MeetingParticipant",
    "MeetingStatus",
    "ParticipantRole",
    "Transcript",
    "ActionItem",
    "ActionItemStatus",
    "KnowledgeNode",
    "KnowledgeEdge",
    "RefreshToken",
    "Note",
    "CalendarIntegration",
    "CalendarEvent",
    "MeetingShare",
    "Comment",
    "AITemplate",
]


def import_models():
    """Import all models for SQLAlchemy metadata"""
    # This function ensures all models are imported
    # so SQLAlchemy can create tables
    pass
