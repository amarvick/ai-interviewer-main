from sqlalchemy.orm import Session

from app.crud.interview import get_interview_session_by_id
from . import flow


class InterviewService:
    """High-level interface for coordinating interview flows."""

    def __init__(self, db: Session):
        self._db = db

    def start_session(self, *, user_id: str, problem_id: str):
        return flow.start_interview_session(
            db=self._db,
            user_id=user_id,
            problem_id=problem_id,
        )

    def get_session(self, session_id: str):
        return get_interview_session_by_id(self._db, session_id)

    def process_message(
        self,
        *,
        session_id: str,
        user_id: str,
        content: str,
        has_submission: bool,
        current_code: str | None,
        chat_history: list[dict[str, str]] | None,
    ):
        return flow.process_interview_message(
            db=self._db,
            session_id=session_id,
            user_id=user_id,
            content=content,
            has_submission=has_submission,
            current_code=current_code,
            chat_history=chat_history,
        )

    def complete_session(
        self,
        *,
        session_id: str,
        user_id: str,
        requested_final_score: float | None = None,
    ):
        return flow.complete_interview_session(
            db=self._db,
            session_id=session_id,
            user_id=user_id,
            requested_final_score=requested_final_score,
        )
