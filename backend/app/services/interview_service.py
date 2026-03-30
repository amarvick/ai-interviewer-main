"""Compatibility layer for legacy imports.

This module now simply re-exports the interview flow functions from the
structured package under ``app.services.interview``. Import from that package
directly in new code.
"""

from app.services.interview import (
    complete_interview_session,
    process_interview_message,
    start_interview_session,
)

__all__ = [
    "start_interview_session",
    "process_interview_message",
    "complete_interview_session",
]
