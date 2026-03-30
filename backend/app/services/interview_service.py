"""Compatibility layer for legacy imports."""

from app.services.interview import (
    InterviewService,
    complete_interview_session,
    process_interview_message,
    start_interview_session,
)

__all__ = [
    "InterviewService",
    "start_interview_session",
    "process_interview_message",
    "complete_interview_session",
]
