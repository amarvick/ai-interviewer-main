from datetime import datetime
import logging
from time import perf_counter
from typing import Any
from app.core.constants import InterviewStage, SUBMISSION_RESULT_PASS
from app.crud.interview import (
    create_interview_evaluation,
    create_interview_message,
    create_interview_session,
    get_interview_session_by_id,
    get_recent_evaluations_by_session_id,
    get_recent_messages_by_session_id,
)
from app.crud.submission import get_latest_submission
from app.crud.testcase import get_testcases_by_problem_id
from app.crud.problem import get_problem_by_id
from app.services.interview_stage_engine import decide_stage_transition
from app.services.interview_ai_service import (
    evaluate_stage_rubric,
    generate_next_interviewer_message,
    generate_failed_submission_guidance,
)
from app.services.analytics import record_interview_evaluation_event
from app.services.interview.helpers import (
    _as_float,
    _as_int,
    _as_stage,
    _as_str,
    _build_budget_rubric_fallback,
    _build_final_feedback,
    _build_recent_context,
    _determine_budget_mode,
    _get_reference_variants,
    _low_budget_assistant_message,
    _match_reference_variant_from_code,
    _maybe_create_local_evaluation,
    _normalize_chat_history,
    _recent_chat_messages,
    _record_ai_usage,
    _serialize_session_detail,
    _wrap_up_prompt_payload,
)

logger = logging.getLogger(__name__)

def start_interview_session(db, user_id: str, problem_id: str):
    start_time = perf_counter()
    problem = get_problem_by_id(db, problem_id)
    if problem is None:
        logger.warning(
            "interview.service.start.problem_not_found user_id=%s problem_id=%s",
            user_id,
            problem_id,
        )
        return None

    session = create_interview_session(db, user_id=user_id, problem_id=problem_id)
    create_interview_message(
        db=db,
        session_id=_as_str(session.id),
        role="assistant",
        content=(
            "Welcome to the interview. Briefly restate the problem in your own words "
            "and ask one clarifying question."
        ),
        stage_at_message=_as_stage(session.stage),
        user_id=None,
    )
    db.commit()
    logger.info(
        "interview.service.start.created user_id=%s session_id=%s problem_id=%s latency_ms=%s",
        user_id,
        _as_str(session.id),
        problem_id,
        int((perf_counter() - start_time) * 1000),
    )
    return get_interview_session_by_id(db, _as_str(session.id))


def process_interview_message(
    db,
    session_id: str,
    user_id: str,
    content: str,
    has_submission: bool,
    current_code: str | None = None,
    chat_history: list[dict[str, str]] | None = None,
):
    start_time = perf_counter()
    session = get_interview_session_by_id(db, session_id)
    if session is None:
        logger.warning(
            "interview.service.message.not_found session_id=%s user_id=%s",
            session_id,
            user_id,
        )
        return None
    if _as_str(session.status) == "COMPLETED":
        logger.info(
            "interview.service.message.already_completed session_id=%s user_id=%s",
            session_id,
            user_id,
        )
        return session

    create_interview_message(
        db=db,
        session_id=_as_str(session.id),
        user_id=user_id,
        role="user",
        content=content,
        stage_at_message=_as_stage(session.stage),
    )

    session = get_interview_session_by_id(db, session_id)
    if session is None:
        return None

    problem_reference = None
    reference_variants: list[dict[str, Any]] = []
    reference_talking_points: list[dict[str, Any]] = []
    if getattr(session, "problem", None) is not None:
        problem_reference = getattr(session.problem, "reference_pseudocode", None)
        reference_variants = _get_reference_variants(session.problem)
        reference_talking_points = (
            getattr(session.problem, "reference_talking_points", None) or []
        )

    current_stage: InterviewStage = _as_stage(session.stage)
    user_turns_in_stage = sum(
        1
        for message in session.messages
        if str(message.role) == "user"
        and _as_stage(message.stage_at_message) == current_stage
    )
    decision = decide_stage_transition(
        current_stage=current_stage,
        latest_user_message=content,
        turn_count_in_stage=user_turns_in_stage,
        stuck_signal_count=session.stuck_signal_count,
        nudges_used_in_stage=session.nudges_used_in_stage,
        has_submission=has_submission,
    )
    effective_decision = decision

    submission_review = (
        _review_latest_submission(
            db=db,
            session=session,
            user_id=user_id,
            has_submission=has_submission,
        )
        if has_submission
        else None
    )
    if submission_review and submission_review["status"] == "fail":
        setattr(session, "stage", "CODING")
        session.status = "ACTIVE"
        session.stuck_signal_count = 0
        session.nudges_used_in_stage = 0
        failure_text = submission_review["assistant_message"]
        create_interview_message(
            db=db,
            session_id=_as_str(session.id),
            role="assistant",
            content=failure_text,
            stage_at_message="CODING",
            user_id=None,
        )
        db.commit()
        logger.info(
            "interview.service.submission_failed session_id=%s user_id=%s test_case=%s",
            session.id,
            user_id,
            submission_review.get("failed_case_label"),
        )
        refreshed_after_failure = get_interview_session_by_id(db, _as_str(session.id))
        if refreshed_after_failure is None:
            return None
        return _serialize_session_detail(refreshed_after_failure, can_code=False)

    previous_stage: InterviewStage = _as_stage(session.stage)
    setattr(session, "stage", effective_decision.next_stage)
    session.stuck_signal_count = effective_decision.stuck_signal_count

    if effective_decision.action == "nudge":
        session.nudges_used_in_stage += 1
    elif effective_decision.action == "advance":
        session.nudges_used_in_stage = 0
    elif effective_decision.action == "stay":
        session.nudges_used_in_stage = session.nudges_used_in_stage

    if effective_decision.next_stage == "COMPLETE":
        session.status = "COMPLETED"
        session.completed_at = datetime.utcnow()

    logger.info(
        "interview.stage.transition session_id=%s user_id=%s from_stage=%s to_stage=%s action=%s "
        "turns_in_stage=%s stuck_signals=%s nudges_used=%s score_stage=%s has_submission=%s",
        session.id,
        user_id,
        previous_stage,
        effective_decision.next_stage,
        effective_decision.action,
        user_turns_in_stage,
        _as_int(session.stuck_signal_count),
        _as_int(session.nudges_used_in_stage),
        effective_decision.should_score_stage,
        has_submission,
    )

    active_variant = _match_reference_variant_from_code(current_code, reference_variants)
    budget_mode = _determine_budget_mode(session)
    usage_tokens = 0
    if _as_stage(session.stage) == "COMPLETE":
        ai_message_payload = _wrap_up_prompt_payload()
    else:
        full_history = _normalize_chat_history(chat_history)
        ai_context = (
            full_history
            if full_history
            else _build_recent_context(db, _as_str(session.id))
        )
        if budget_mode == "exhausted":
            ai_message_payload = _low_budget_assistant_message(_as_stage(session.stage))
        else:
            ai_message_payload, usage_tokens = generate_next_interviewer_message(
                recent_messages=ai_context,
                current_code=current_code,
                reference_pseudocode=problem_reference,
                reference_variants=reference_variants,
                active_variant=active_variant,
                budget_mode="lightweight" if budget_mode == "lightweight" else "default",
            )
            _record_ai_usage(session, usage_tokens)
    create_interview_message(
        db=db,
        session_id=_as_str(session.id),
        role="assistant",
        content=ai_message_payload["assistant_message"],
        stage_at_message=_as_stage(session.stage),
        user_id=None,
    )
    if bool(ai_message_payload.get("should_end_interview", False)):
        session.status = "COMPLETED"
        setattr(session, "stage", "COMPLETE")
        session.completed_at = datetime.utcnow()
        logger.info(
            "interview.service.ai_completed session_id=%s user_id=%s",
            _as_str(session.id),
            user_id,
        )

    db.commit()
    logger.info(
        "interview.service.message.completed session_id=%s user_id=%s stage=%s latency_ms=%s",
        session.id,
        user_id,
        session.stage,
        int((perf_counter() - start_time) * 1000),
    )
    refreshed = get_interview_session_by_id(db, _as_str(session.id))
    if refreshed is None:
        return None
    return _serialize_session_detail(
        refreshed,
        can_code=bool(ai_message_payload.get("can_code", False)),
    )


def complete_interview_session(
    db,
    session_id: str,
    user_id: str,
    requested_final_score: float | None = None,
):
    start_time = perf_counter()
    session = get_interview_session_by_id(db, session_id)
    if session is None:
        logger.warning(
            "interview.service.complete.not_found session_id=%s user_id=%s",
            session_id,
            user_id,
        )
        return None
    if _as_str(session.user_id) != user_id:
        logger.warning(
            "interview.service.complete.forbidden session_id=%s user_id=%s owner_user_id=%s",
            session_id,
            user_id,
            session.user_id,
        )
        return None

    latest_submission = get_latest_submission(
        db=db,
        user_id=user_id,
        problem_id=_as_str(session.problem_id),
    )
    final_code_snapshot = latest_submission.code_submitted if latest_submission else None
    final_tests_passed = (
        _as_int(latest_submission.tests_passed) if latest_submission else None
    )
    final_tests_total = (
        _as_int(latest_submission.tests_total) if latest_submission else None
    )

    problem_reference = None
    reference_variants: list[dict[str, Any]] = []
    reference_talking_points: list[dict[str, Any]] = []
    if getattr(session, "problem", None) is not None:
        problem_reference = getattr(session.problem, "reference_pseudocode", None)
        reference_variants = _get_reference_variants(session.problem)
        reference_talking_points = (
            getattr(session.problem, "reference_talking_points", None) or []
        )

    stage_messages = [
        {"role": _as_str(message.role), "content": _as_str(message.content)}
        for message in session.messages
        if _as_str(message.role) in {"user", "assistant"}
    ]
    has_transcript = bool(stage_messages)

    evaluations = get_recent_evaluations_by_session_id(db, _as_str(session.id), limit=500)
    if not evaluations and not has_transcript:
        created_local_eval = _maybe_create_local_evaluation(
            db=db,
            session=session,
            latest_submission=latest_submission,
            reference_variants=reference_variants,
        )
        if created_local_eval:
            evaluations = get_recent_evaluations_by_session_id(
                db, _as_str(session.id), limit=500
            )

    if not evaluations and has_transcript:
        if stage_messages:
            try:
                active_variant = _match_reference_variant_from_code(
                    final_code_snapshot, reference_variants
                )
                budget_mode = _determine_budget_mode(session)
                source_label = "llm_eval_final"
                rubric_tokens = 0
                if budget_mode == "exhausted":
                    final_rubric = _build_budget_rubric_fallback(
                        tests_passed=final_tests_passed,
                        tests_total=final_tests_total,
                    )
                    source_label = "budget_fallback"
                else:
                    final_rubric, rubric_tokens = evaluate_stage_rubric(
                        stage_messages=stage_messages,
                        current_code=final_code_snapshot,
                        reference_pseudocode=problem_reference,
                        reference_talking_points=reference_talking_points,
                        reference_variants=reference_variants,
                        active_variant=active_variant,
                        budget_mode="lightweight"
                        if budget_mode == "lightweight"
                        else "default",
                    )
                    _record_ai_usage(session, rubric_tokens)
                final_total = (
                    final_rubric["problem_understanding_score"]
                    + final_rubric["approach_quality_score"]
                    + final_rubric["code_correctness_reasoning_score"]
                    + final_rubric["complexity_analysis_score"]
                    + final_rubric["communication_clarity_score"]
                )
                create_interview_evaluation(
                    db=db,
                    session_id=_as_str(session.id),
                    stage="FEEDBACK",
                    summary=final_rubric.get(
                        "summary", "Final interview evaluation generated."
                    ),
                    problem_understanding_score=final_rubric[
                        "problem_understanding_score"
                    ],
                    approach_quality_score=final_rubric["approach_quality_score"],
                    code_correctness_reasoning_score=final_rubric[
                        "code_correctness_reasoning_score"
                    ],
                    complexity_analysis_score=final_rubric[
                        "complexity_analysis_score"
                    ],
                    communication_clarity_score=final_rubric[
                        "communication_clarity_score"
                    ],
                    total_score=final_total,
                    passed=final_total >= 30,
                    rubric_json={
                        "source": "llm_eval_final",
                        "tests_passed": final_tests_passed,
                        "tests_total": final_tests_total,
                        **final_rubric,
                    },
                )
                session_problem_id = getattr(session, "problem_id", None)
                session_user_id = getattr(session, "user_id", None)
                record_interview_evaluation_event(
                    session_id=_as_str(session.id),
                    problem_id=_as_str(session_problem_id)
                    if session_problem_id
                    else None,
                    user_id=_as_str(session_user_id) if session_user_id else None,
                    source=source_label,
                    total_score=final_total,
                    rubric_scores={
                        "problem_understanding_score": final_rubric[
                            "problem_understanding_score"
                        ],
                        "approach_quality_score": final_rubric[
                            "approach_quality_score"
                        ],
                        "code_correctness_reasoning_score": final_rubric[
                            "code_correctness_reasoning_score"
                        ],
                        "complexity_analysis_score": final_rubric[
                            "complexity_analysis_score"
                        ],
                        "communication_clarity_score": final_rubric[
                            "communication_clarity_score"
                        ],
                    },
                    variant=active_variant,
                    metadata={
                        "tests_passed": final_tests_passed,
                        "tests_total": final_tests_total,
                        "budget_mode": budget_mode,
                        "rubric_tokens": rubric_tokens,
                    },
                )
                db.flush()
            except Exception:
                logger.exception(
                    "interview.service.complete.final_rubric_failed session_id=%s",
                    _as_str(session.id),
                )
                fallback_created = _maybe_create_local_evaluation(
                    db=db,
                    session=session,
                    latest_submission=latest_submission,
                    reference_variants=reference_variants,
                )
                if fallback_created:
                    evaluations = get_recent_evaluations_by_session_id(
                        db, _as_str(session.id), limit=500
                    )
        evaluations = get_recent_evaluations_by_session_id(
            db, _as_str(session.id), limit=500
        )
    computed_score = requested_final_score
    if computed_score is None:
        if evaluations:
            average_total = sum(e.total_score for e in evaluations) / len(evaluations)
            computed_score = average_total
        else:
            computed_score = 0

    session.final_score = round(float(computed_score), 2)
    session.status = "COMPLETED"
    setattr(session, "stage", "COMPLETE")
    session.completed_at = datetime.utcnow()
    db.commit()
    refreshed = get_interview_session_by_id(db, _as_str(session.id))
    if refreshed is None:
        return None
    feedback = _build_final_feedback(evaluations)
    logger.info(
        "interview.service.complete.completed session_id=%s user_id=%s final_score=%s eval_count=%s latency_ms=%s",
        session.id,
        user_id,
        _as_float(session.final_score),
        len(evaluations),
        int((perf_counter() - start_time) * 1000),
    )
    return {
        "id": refreshed.id,
        "user_id": _as_str(refreshed.user_id),
        "problem_id": _as_str(refreshed.problem_id),
        "stage": _as_stage(refreshed.stage),
        "status": _as_str(refreshed.status),
        "final_score": _as_float(refreshed.final_score),
        "stuck_signal_count": _as_int(refreshed.stuck_signal_count),
        "nudges_used_in_stage": _as_int(refreshed.nudges_used_in_stage),
        "started_at": refreshed.started_at,
        "completed_at": refreshed.completed_at,
        "created_at": refreshed.created_at,
        "updated_at": refreshed.updated_at,
        "strengths": feedback["strengths"],
        "gaps": feedback["gaps"],
        "next_steps": feedback["next_steps"],
    }

def _review_latest_submission(db, session, user_id: str, has_submission: bool) -> dict[str, Any] | None:
    if not has_submission:
        return None
    latest = get_latest_submission(
        db=db,
        user_id=user_id,
        problem_id=_as_str(session.problem_id),
    )
    if latest is None:
        return None
    if _as_str(latest.result) == SUBMISSION_RESULT_PASS:
        return {"status": "pass"}

    testcases = get_testcases_by_problem_id(db, _as_str(session.problem_id))
    tests_passed = _as_int(latest.tests_passed)
    failing_case = None
    if testcases and 0 <= tests_passed < len(testcases):
        failing_case = testcases[tests_passed]
    failure_context = {
        "case_index": tests_passed + 1,
        "case_total": len(testcases),
        "params": getattr(failing_case, "params", None) if failing_case else None,
        "expected_output": getattr(failing_case, "expected_output", None)
        if failing_case
        else None,
        "language": _as_str(latest.language),
        "error_message": _as_str(latest.error or "Test failure"),
    }
    guidance = generate_failed_submission_guidance(
        recent_messages=_recent_chat_messages(session.messages),
        failure_context=failure_context,
    )
    case_label = None
    if failure_context.get("case_index") and failure_context.get("case_total"):
        case_label = f"{failure_context['case_index']}/{failure_context['case_total']}"
    return {
        "status": "fail",
        "assistant_message": guidance["assistant_message"],
        "failed_case_label": case_label,
    }
