from __future__ import annotations

from datetime import datetime
from typing import Any, cast

from app.core.constants import InterviewStage
from app.crud.interview import (
    create_interview_evaluation,
    get_recent_evaluations_by_session_id,
    get_recent_messages_by_session_id,
)
from app.services.analytics import record_interview_evaluation_event


AI_TOKEN_LIGHTWEIGHT_THRESHOLD = 12000
AI_TOKEN_HARD_LIMIT = 16000


def _as_stage(value: Any) -> InterviewStage:
    stage = str(value)
    valid: set[str] = {
        "INTRO",
        "CLARIFICATION",
        "APPROACH_DISCUSSION",
        "PSEUDOCODE",
        "CODING",
        "COMPLEXITY_DISCUSSION",
        "FOLLOW_UP",
        "FEEDBACK",
        "COMPLETE",
    }
    if stage not in valid:
        return "INTRO"
    return cast(InterviewStage, stage)


def _as_str(value: Any) -> str:
    return str(value)


def _as_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _as_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _wrap_up_prompt_payload() -> dict[str, Any]:
    return {
        "assistant_message": (
            "Great job driving the solution to completion. Before we wrap up, is there anything else you'd add—"
            "maybe an alternative approach, additional tests, or trade-offs worth mentioning?"
        ),
        "checklist": {
            "clarified_constraints": True,
            "proposed_approach": True,
            "complexity_analyzed": True,
            "ready_to_code": True,
        },
        "can_code": False,
        "should_end_interview": True,
    }


def _build_recent_context(db, session_id: str) -> list[dict[str, str]]:
    recent_messages = get_recent_messages_by_session_id(db, session_id, limit=8)
    recent_messages = list(reversed(recent_messages))
    recent_evaluations = get_recent_evaluations_by_session_id(db, session_id, limit=3)

    context: list[dict[str, str]] = [
        {"role": _as_str(message.role), "content": _as_str(message.content)}
        for message in recent_messages
    ]
    if recent_evaluations:
        summary_lines = [
            f"{_as_str(evaluation.stage)}: {_as_str(evaluation.summary or 'No summary')}"
            for evaluation in reversed(recent_evaluations)
        ]
        context.insert(
            0,
            {
                "role": "system",
                "content": "Recent evaluation summaries:\n" + "\n".join(summary_lines),
            },
        )
    return context


def _recent_chat_messages(messages, limit: int = 6) -> list[dict[str, str]]:
    ordered = sorted(messages, key=lambda m: m.created_at or datetime.utcnow())
    excerpt = ordered[-limit:]
    turns: list[dict[str, str]] = []
    for message in excerpt:
        role = _as_str(message.role)
        if role not in {"user", "assistant"}:
            continue
        turns.append(
            {
                "role": "user" if role == "user" else "assistant",
                "content": _as_str(message.content),
            }
        )
    return turns


def _get_reference_variants(problem) -> list[dict[str, Any]]:
    raw_variants = getattr(problem, "reference_pseudocode_variants", None)
    normalized: list[dict[str, Any]] = []
    if isinstance(raw_variants, list) and raw_variants:
        for index, variant in enumerate(raw_variants):
            if not isinstance(variant, dict):
                continue
            normalized.append(
                {
                    "id": str(variant.get("id") or f"variant_{index+1}"),
                    "title": str(variant.get("title") or f"Variant {index+1}"),
                    "pseudocode": str(variant.get("pseudocode") or ""),
                    "is_optimal": bool(variant.get("is_optimal", False)),
                    "match_signals": [
                        str(signal).lower()
                        for signal in (variant.get("match_signals") or [])
                        if isinstance(signal, str) and signal.strip()
                    ],
                    "complexity": (
                        str(variant.get("complexity")).strip()
                        if variant.get("complexity")
                        else None
                    ),
                    "notes": (
                        str(variant.get("notes")).strip()
                        if variant.get("notes")
                        else None
                    ),
                    "strengths": [
                        str(item).strip()
                        for item in (variant.get("strengths") or [])
                        if str(item).strip()
                    ],
                    "improvements": [
                        str(item).strip()
                        for item in (variant.get("improvements") or [])
                        if str(item).strip()
                    ],
                }
            )
    elif getattr(problem, "reference_pseudocode", None):
        normalized.append(
            {
                "id": "primary",
                "title": "Reference solution",
                "pseudocode": str(problem.reference_pseudocode),
                "is_optimal": True,
                "match_signals": [],
                "strengths": [],
                "improvements": [],
                "complexity": None,
                "notes": None,
            }
        )
    return normalized


def _match_reference_variant_from_code(
    code: str | None, reference_variants: list[dict[str, Any]]
) -> dict[str, Any] | None:
    if not code or not reference_variants:
        return None
    normalized_code = code.lower()
    fallback_variant = next(
        (variant for variant in reference_variants if variant.get("is_optimal")), None
    ) or (reference_variants[0] if reference_variants else None)
    for variant in reference_variants:
        signals = variant.get("match_signals") or []
        if not signals:
            continue
        for signal in signals:
            if signal and signal in normalized_code:
                return variant
    return fallback_variant


def _maybe_create_local_evaluation(
    db,
    session,
    latest_submission,
    reference_variants: list[dict[str, Any]],
) -> bool:
    if latest_submission is None or not reference_variants:
        return False
    tests_total = _as_int(latest_submission.tests_total)
    tests_passed = _as_int(latest_submission.tests_passed)
    if tests_total <= 0 or tests_passed < tests_total:
        return False

    matched_variant = _match_reference_variant_from_code(
        latest_submission.code_submitted, reference_variants
    )
    if matched_variant is None:
        return False

    scores = _build_local_score_profile(matched_variant)
    total_score = sum(scores.values())
    summary = _build_local_summary(matched_variant, total_score)
    strengths = matched_variant.get("strengths") or [
        "All automated tests passed on the first submission.",
        f"Implemented the {matched_variant['title']} approach reliably.",
    ]
    improvements = matched_variant.get("improvements") or [
        "Call out trade-offs when comparing against alternative strategies."
    ]
    create_interview_evaluation(
        db=db,
        session_id=_as_str(session.id),
        stage="FEEDBACK",
        summary=summary,
        problem_understanding_score=scores["problem_understanding_score"],
        approach_quality_score=scores["approach_quality_score"],
        code_correctness_reasoning_score=scores["code_correctness_reasoning_score"],
        complexity_analysis_score=scores["complexity_analysis_score"],
        communication_clarity_score=scores["communication_clarity_score"],
        total_score=total_score,
        passed=total_score >= 30,
        rubric_json={
            "source": "local_heuristic",
            "tests_passed": tests_passed,
            "tests_total": tests_total,
            "reference_variant": matched_variant,
            "summary": summary,
            "strengths": strengths,
            "additional_improvements": improvements,
        },
    )
    session_problem_id = getattr(session, "problem_id", None)
    session_user_id = getattr(session, "user_id", None)
    record_interview_evaluation_event(
        session_id=_as_str(session.id),
        problem_id=_as_str(session_problem_id) if session_problem_id else None,
        user_id=_as_str(session_user_id) if session_user_id else None,
        source="local_heuristic",
        total_score=total_score,
        rubric_scores={
            "problem_understanding_score": scores["problem_understanding_score"],
            "approach_quality_score": scores["approach_quality_score"],
            "code_correctness_reasoning_score": scores[
                "code_correctness_reasoning_score"
            ],
            "complexity_analysis_score": scores["complexity_analysis_score"],
            "communication_clarity_score": scores["communication_clarity_score"],
        },
        variant=matched_variant,
        metadata={
            "tests_total": tests_total,
            "tests_passed": tests_passed,
            "summary": summary,
        },
    )
    return True


def _build_local_score_profile(variant: dict[str, Any]) -> dict[str, int]:
    if bool(variant.get("is_optimal")):
        return {
            "problem_understanding_score": 9,
            "approach_quality_score": 10,
            "code_correctness_reasoning_score": 10,
            "complexity_analysis_score": 9,
            "communication_clarity_score": 9,
        }
    return {
        "problem_understanding_score": 8,
        "approach_quality_score": 7,
        "code_correctness_reasoning_score": 10,
        "complexity_analysis_score": 7,
        "communication_clarity_score": 8,
    }


def _build_local_summary(variant: dict[str, Any], total_score: int) -> str:
    pieces = [
        f"The candidate implemented the {variant.get('title', 'reference')} approach"
    ]
    complexity = variant.get("complexity")
    if complexity:
        pieces.append(f"({complexity})")
    pieces.append("and passed all automated tests on the first try.")
    if not variant.get("is_optimal"):
        pieces.append(
            "It is acceptable but slower than the optimal hash map approach, so call out trade-offs more explicitly."
        )
    return " ".join(pieces) + f" Total score: {total_score}/50."


def _determine_budget_mode(session) -> str:
    total = _as_int(getattr(session, "ai_token_total", 0))
    if total >= AI_TOKEN_HARD_LIMIT:
        return "exhausted"
    if total >= AI_TOKEN_LIGHTWEIGHT_THRESHOLD:
        return "lightweight"
    return "default"


def _record_ai_usage(session, tokens_used: int) -> None:
    if not tokens_used:
        return
    current = _as_int(getattr(session, "ai_token_total", 0))
    session.ai_token_total = current + int(tokens_used)


def _low_budget_assistant_message(stage: InterviewStage) -> dict[str, Any]:
    return {
        "assistant_message": (
            "We're nearly out of time, so let's keep responses short. "
            "Share any final thoughts or edge cases, and I'll summarize."
        ),
        "checklist": {
            "clarified_constraints": stage != "INTRO",
            "proposed_approach": stage not in {"INTRO", "CLARIFICATION"},
            "complexity_analyzed": stage
            in {"COMPLEXITY_DISCUSSION", "FOLLOW_UP", "FEEDBACK", "COMPLETE"},
            "ready_to_code": stage in {"CODING", "FOLLOW_UP", "FEEDBACK", "COMPLETE"},
        },
        "can_code": stage in {"CODING", "FOLLOW_UP", "FEEDBACK", "COMPLETE"},
        "internal_thought": "Budget exhausted fallback response.",
        "should_end_interview": stage in {"FEEDBACK", "COMPLETE"},
    }


def _build_budget_rubric_fallback(
    tests_passed: int | None, tests_total: int | None
) -> dict[str, Any]:
    all_tests_passed = (
        tests_passed is not None
        and tests_total is not None
        and tests_total > 0
        and tests_passed >= tests_total
    )
    base_score = 9 if all_tests_passed else 7
    summary = (
        "AI token budget exhausted before generating a rubric. "
        "Using deterministic fallback based on submission results."
    )
    return {
        "problem_understanding_score": base_score - 1,
        "approach_quality_score": base_score,
        "code_correctness_reasoning_score": base_score + (1 if all_tests_passed else 0),
        "complexity_analysis_score": base_score - 1,
        "communication_clarity_score": base_score - 1,
        "summary": summary,
        "strengths": [
            "Submission passed all automated tests."
            if all_tests_passed
            else "Submission progress recorded before budget ran out.",
            "Maintained steady communication through the interview.",
        ],
        "additional_improvements": [
            "Highlight at least two edge cases before coding.",
            "State time/space complexity explicitly even when the solution is optimal.",
            "Share one trade-off versus an alternative approach.",
        ],
    }


def _normalize_chat_history(
    chat_history: list[dict[str, str]] | None,
) -> list[dict[str, str]]:
    if not chat_history:
        return []
    normalized: list[dict[str, str]] = []
    for turn in chat_history:
        role = str(turn.get("role", "")).strip().lower()
        content = str(turn.get("content", "")).strip()
        if role not in {"user", "assistant", "system"} or not content:
            continue
        normalized.append({"role": role, "content": content})
    return normalized


def _serialize_session_detail(session, can_code: bool) -> dict[str, Any]:
    return {
        "id": _as_str(session.id),
        "user_id": _as_str(session.user_id),
        "problem_id": _as_str(session.problem_id),
        "stage": _as_stage(session.stage),
        "status": _as_str(session.status),
        "final_score": _as_float(session.final_score),
        "stuck_signal_count": _as_int(session.stuck_signal_count),
        "nudges_used_in_stage": _as_int(session.nudges_used_in_stage),
        "started_at": session.started_at,
        "completed_at": session.completed_at,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
        "messages": session.messages,
        "evaluations": session.evaluations,
        "can_code": can_code,
    }


def _build_final_feedback(evaluations: list) -> dict[str, list[str]]:
    if not evaluations:
        return {
            "strengths": ["You completed the interview flow."],
            "gaps": ["Not enough rubric data yet to identify specific gaps."],
            "next_steps": [
                "Complete another interview run with fuller explanations per stage."
            ],
        }

    category_totals = {
        "problem_understanding": 0.0,
        "approach_quality": 0.0,
        "code_correctness_reasoning": 0.0,
        "complexity_analysis": 0.0,
        "communication_clarity": 0.0,
    }
    for evaluation in evaluations:
        category_totals["problem_understanding"] += evaluation.problem_understanding_score
        category_totals["approach_quality"] += evaluation.approach_quality_score
        category_totals["code_correctness_reasoning"] += (
            evaluation.code_correctness_reasoning_score
        )
        category_totals["complexity_analysis"] += evaluation.complexity_analysis_score
        category_totals["communication_clarity"] += evaluation.communication_clarity_score

    count = float(len(evaluations))
    category_averages = {key: value / count for key, value in category_totals.items()}
    ordered_best = sorted(category_averages.items(), key=lambda item: item[1], reverse=True)
    ordered_low = [
        item for item in sorted(category_averages.items(), key=lambda item: item[1]) if item[1] < 7.0
    ]

    label = {
        "problem_understanding": "Problem understanding",
        "approach_quality": "Approach quality",
        "code_correctness_reasoning": "Correctness reasoning",
        "complexity_analysis": "Complexity analysis",
        "communication_clarity": "Communication clarity",
    }
    next_step_by_gap = {
        "problem_understanding": "Restate requirements and list at least 3 edge cases before coding.",
        "approach_quality": "Compare one alternative approach and justify your final choice.",
        "code_correctness_reasoning": "Explain one invariant and walk through one concrete test trace.",
        "complexity_analysis": "State exact time/space Big-O and tie it to each major operation.",
        "communication_clarity": "Answer in short structured bullets: plan, why, tradeoff.",
    }
    ai_strengths: list[str] = []
    ai_improvements: list[str] = []
    for evaluation in reversed(evaluations):
        rubric_json = getattr(evaluation, "rubric_json", None)
        if isinstance(rubric_json, dict):
            raw_strengths = rubric_json.get("strengths")
            if isinstance(raw_strengths, list):
                for item in raw_strengths:
                    text = str(item).strip()
                    if text:
                        ai_strengths.append(text)
            raw_improvements = rubric_json.get("additional_improvements")
            if isinstance(raw_improvements, list):
                for item in raw_improvements:
                    text = str(item).strip()
                    if text:
                        ai_improvements.append(text)

    strengths = list(dict.fromkeys(ai_strengths))[:3]
    if not strengths:
        strengths = [f"{label[key]} ({avg:.2f}/10)" for key, avg in ordered_best[:2]]
    improvements_unique = list(dict.fromkeys(ai_improvements))
    gaps = improvements_unique[:3]
    next_steps = improvements_unique[3:6]
    if not gaps:
        fallback_low = ordered_low or ordered_best[-2:]
        gaps = [
            f"Focus on {label[key].lower()} by {next_step_by_gap[key]}"
            for key, _ in fallback_low[:2]
        ]
    if not next_steps:
        target_categories = ordered_low[:3] or ordered_best[:2]
        next_steps = [next_step_by_gap[key] for key, _ in target_categories]

    return {"strengths": strengths, "gaps": gaps, "next_steps": next_steps}


__all__ = [
    "AI_TOKEN_HARD_LIMIT",
    "AI_TOKEN_LIGHTWEIGHT_THRESHOLD",
    "_as_stage",
    "_as_str",
    "_as_int",
    "_as_float",
    "_wrap_up_prompt_payload",
    "_build_recent_context",
    "_recent_chat_messages",
    "_get_reference_variants",
    "_match_reference_variant_from_code",
    "_maybe_create_local_evaluation",
    "_determine_budget_mode",
    "_record_ai_usage",
    "_low_budget_assistant_message",
    "_build_budget_rubric_fallback",
    "_build_local_score_profile",
    "_build_local_summary",
    "_normalize_chat_history",
    "_serialize_session_detail",
    "_build_final_feedback",
]
