import json
import logging
from typing import Any, Mapping

analytics_logger = logging.getLogger("analytics")


def _score_band(value: float | int | None) -> str:
    if value is None:
        return "unknown"
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return "unknown"
    if numeric >= 9:
        return "9-10"
    if numeric >= 8:
        return "8-9"
    if numeric >= 6.5:
        return "6.5-8"
    return "0-6.5"


def record_interview_evaluation_event(
    *,
    session_id: str,
    problem_id: str | None,
    user_id: str | None,
    source: str,
    total_score: float | int | None,
    rubric_scores: Mapping[str, Any],
    variant: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> None:
    if not session_id:
        return
    payload = {
        "session_id": session_id,
        "problem_id": problem_id,
        "user_id": user_id,
        "source": source,
        "total_score": total_score,
        "score_band": _score_band(total_score),
        "rubric_band": {
            key: _score_band(value)
            for key, value in rubric_scores.items()
            if isinstance(value, (int, float))
        },
        "variant": {
            "id": variant.get("id"),
            "title": variant.get("title"),
            "is_optimal": variant.get("is_optimal"),
        }
        if variant
        else None,
        "metadata": metadata or {},
    }
    analytics_logger.info(
        "analytics.interview.evaluation %s",
        json.dumps(payload, default=str),
    )
