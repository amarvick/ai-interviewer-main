from __future__ import annotations
import logging
from typing import Any, TypedDict, cast, Literal

from google import genai
from google.genai import types
from pydantic import BaseModel, Field

from app.core.config import INTERVIEW_AI_MODE, GEMINI_API_KEY, GEMINI_MODEL_CHAT

BAND_SCORES: dict[str, int] = {
    "excellent": 10,
    "strong": 8,
    "fair": 6,
    "weak": 4,
    "poor": 2,
}
BAND_ORDER = list(BAND_SCORES.keys())

logger = logging.getLogger(__name__)

class InterviewAIError(RuntimeError):
    pass

class ChatTurn(TypedDict):
    role: str
    content: str

# TODO - put these in schemas

class InterviewChecklist(BaseModel):
    clarified_constraints: bool = Field(description="User understands input/output and edge cases")
    proposed_approach: bool = Field(description="User explained the high-level logic and algorithm")
    complexity_analyzed: bool = Field(description="User discussed Big-O Time and Space complexity")
    ready_to_code: bool = Field(description="Set to true ONLY when all above are True")

class InterviewerResponse(BaseModel):
    assistant_message: str = Field(description="The text shown to the candidate")
    checklist_status: InterviewChecklist
    internal_thought: str = Field(description="Your reasoning for why you are asking this specific question")
    confidence: str # low, medium, high
    should_end_interview: bool = False

class RubricResponse(BaseModel):
    problem_understanding_band: str
    approach_quality_band: str
    code_correctness_reasoning_band: str
    complexity_analysis_band: str
    communication_clarity_band: str
    summary: str
    strengths: list[str] = Field(default_factory=list)
    additional_improvements: list[str] = Field(default_factory=list)


class SubmissionFailureResponse(BaseModel):
    assistant_message: str
    next_steps: list[str] = Field(default_factory=list)

def generate_next_interviewer_message(
    recent_messages: list[ChatTurn],
    current_code: str | None = None,
    reference_pseudocode: str | None = None,
    reference_variants: list[dict[str, Any]] | None = None,
    active_variant: dict[str, Any] | None = None,
    budget_mode: Literal["default", "lightweight"] = "default",
) -> tuple[dict[str, Any], int]:
    client = _build_client()
    if not client:
        if _is_strict_mode(): raise InterviewAIError("Gemini API key missing.")
        return _fallback_interviewer_message()

    system_instruction = (
        "You are an elite Technical Interviewer. Guide the candidate through an algorithm interview.\n\n"
        "GOAL: Ensure the candidate explains the problem, edge cases, and complexity BEFORE they start coding.\n"
        "RULES:\n"
        "1. PROACTIVITY: If they code too early, ask them to discuss complexity first.\n"
        "2. CONCISENESS: Keep responses under 60 words.\n"
        "3. STATE: Update the 'checklist_status' based on the history.\n"
        "4. NO SPOILERS: Never provide the full solution code.\n"
        "5. Ask the candidate for at least one concise dry-run walkthrough when useful.\n"
        "6. If the interview is complete, do NOT ask to move to another question. "
        "Provide a short closing line and set should_end_interview=true."
    )
    variant_context = ""
    if active_variant and active_variant.get("pseudocode"):
        variant_context = (
            f"\nREFERENCE APPROACH IN PLAY: {active_variant.get('title', 'Selected variant')}."
            f"\nComplexity: {active_variant.get('complexity', 'n/a')}."
            f"\nPseudocode (keep private):\n{active_variant['pseudocode']}"
        )
    elif reference_pseudocode:
        variant_context = (
            "\nREFERENCE PSEUDOCODE (do not reveal verbatim; use it to guide evaluation):\n"
            f"{reference_pseudocode.strip()}"
        )
    elif reference_variants:
        bullet_lines = "\n".join(
            f"- {variant.get('title', 'Variant')}: {variant.get('complexity', 'n/a')}"
            for variant in reference_variants[:3]
        )
        variant_context = f"\nREFERENCE APPROACHES:\n{bullet_lines}"
    system_instruction += variant_context
    if budget_mode == "lightweight":
        system_instruction += (
            "\nTOKEN CONSERVATION MODE: reply in <=35 words, avoid repeating prior context, "
            "and prioritize the single most important coaching point."
        )

    contents = _prepare_contents(recent_messages, current_code)

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL_CHAT,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.4,
                response_mime_type="application/json",
                response_schema=InterviewerResponse,
            ),
        )
        
        parsed = cast(InterviewerResponse, response.parsed)
        usage_tokens = _log_usage(response, "interview_chat")

        return ({
            "assistant_message": parsed.assistant_message,
            "checklist": parsed.checklist_status.model_dump(),
            "can_code": parsed.checklist_status.ready_to_code,
            "internal_thought": parsed.internal_thought,
            "should_end_interview": bool(parsed.should_end_interview),
        }, usage_tokens)
    except Exception as exc:
        logger.exception("Gemini error")
        if _is_quota_error(exc):
            raise InterviewAIError(
                "AI quota exceeded. Please check your Gemini billing/quota and try again."
            ) from exc
        if _is_strict_mode():
            raise InterviewAIError(
                f"Gemini message generation failed: {type(exc).__name__}"
            ) from exc
        return _fallback_interviewer_message(), 0

def evaluate_stage_rubric(
    stage_messages: list[ChatTurn],
    current_code: str | None = None,
    reference_pseudocode: str | None = None,
    reference_variants: list[dict[str, Any]] | None = None,
    active_variant: dict[str, Any] | None = None,
    budget_mode: Literal["default", "lightweight"] = "default",
) -> tuple[dict[str, Any], int]:
    client = _build_client()
    if not client:
        return _fallback_rubric("Rubric evaluator unavailable.")

    transcript = "\n".join([f"{m['role']}: {m['content']}" for m in stage_messages])
    reference_context = ""
    if active_variant and active_variant.get("pseudocode"):
        reference_context = (
            f"Reference approach ({active_variant.get('title', 'variant')}) "
            f"{active_variant.get('complexity', '')}:\n"
            f"{active_variant['pseudocode']}\n\n"
        )
    elif reference_pseudocode:
        reference_context = (
            f"Reference pseudocode (keep private):\n{reference_pseudocode.strip()}\n\n"
        )
    elif reference_variants:
        reference_context = "Reference approaches:\n" + "\n".join(
            f"- {variant.get('title', 'Variant')}: {variant.get('pseudocode', '')[:200]}"
            for variant in reference_variants[:2]
        ) + "\n\n"
    code_context = f"\n\nCode Snapshot:\n{current_code}" if current_code else ""

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL_CHAT,
            contents=f"{reference_context}Review this transcript and code:\n{transcript}{code_context}",
            config=types.GenerateContentConfig(
                system_instruction=_build_rubric_instruction(budget_mode),
                response_mime_type="application/json",
                response_schema=RubricResponse,
            ),
        )
        parsed = cast(RubricResponse | None, response.parsed)
        if parsed is None:
            raise ValueError("Missing parsed rubric response")
        usage_tokens = _log_usage(response, "interview_rubric")
        return _normalize_rubric(parsed.model_dump()), usage_tokens
    except Exception as exc:
        logger.exception("Gemini rubric evaluation failed")
        if _is_quota_error(exc):
            raise InterviewAIError(
                "AI quota exceeded. Please check your Gemini billing/quota and try again."
            ) from exc
        if _is_strict_mode():
            raise InterviewAIError(
                f"Gemini rubric evaluation failed: {type(exc).__name__}"
            ) from exc
        return _fallback_rubric(f"Automatic fallback used ({type(exc).__name__})."), 0

def _prepare_contents(messages: list[ChatTurn], code: str | None) -> list[types.Content]:
    contents = []
    for m in messages[-10:]:
        role = "user" if m["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part.from_text(text=m["content"])]))
    
    if code:
        contents.append(types.Content(
            role="user",
            parts=[types.Part.from_text(text=f"SYSTEM NOTE: Current Code State:\n{code[:5000]}")]
        ))
    return contents

def _build_rubric_instruction(budget_mode: Literal["default", "lightweight"]) -> str:
    instruction = (
        "Assign a qualitative band for each category using ONLY these labels: "
        "excellent, strong, fair, weak, poor. "
        "Return strict JSON with the following keys: "
        "problem_understanding_band, approach_quality_band, code_correctness_reasoning_band, "
        "complexity_analysis_band, communication_clarity_band, summary, strengths (2-4 items), "
        "additional_improvements (3-5 items). "
        "Highlight wins first, then the biggest gap."
    )
    if budget_mode == "lightweight":
        instruction += " Keep summary under 60 words and avoid restating the problem."
    return instruction

def _build_client():
    return genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

def _log_usage(response: Any, label: str) -> int:
    usage = getattr(response, "usage_metadata", None)
    tokens = 0
    if usage:
        tokens = int(getattr(usage, "total_token_count", 0) or 0)
        logger.info(f"Gemini Usage [{label}]: {tokens} tokens")
    return tokens

def _is_strict_mode() -> bool:
    return INTERVIEW_AI_MODE == "strict"


def _is_quota_error(exc: Exception) -> bool:
    text = str(exc).lower()
    markers = (
        "quota",
        "resource_exhausted",
        "rate limit",
        "429",
        "insufficient",
        "billing",
    )
    return any(marker in text for marker in markers)

def _fallback_interviewer_message() -> dict[str, Any]:
    return {
        "assistant_message": "Tell me more about your approach.",
        "checklist": {"clarified_constraints": False, "proposed_approach": False, "complexity_analyzed": False, "ready_to_code": False},
        "can_code": False,
        "should_end_interview": False,
    }

def _fallback_rubric(reason: str | None = None) -> dict[str, Any]:
    summary = (
        reason
        if reason
        else "Automatic rubric fallback used."
    )
    return {
        "problem_understanding_score": 5,
        "approach_quality_score": 5,
        "code_correctness_reasoning_score": 5,
        "complexity_analysis_score": 5,
        "communication_clarity_score": 5,
        "summary": summary,
        "strengths": [
            "Candidate engaged with the prompt and kept the discussion moving.",
            "Candidate attempted to reason about the solution structure.",
        ],
        "additional_improvements": [
            "Use a short structure for answers: approach, correctness, complexity.",
            "State at least 2 edge cases before coding and validate them after coding.",
            "Explain one tradeoff versus an alternative approach.",
        ],
    }


def _normalize_rubric(raw: dict[str, Any]) -> dict[str, Any]:
    return {
        "problem_understanding_score": _band_to_score(
            raw.get("problem_understanding_band")
        ),
        "approach_quality_score": _band_to_score(raw.get("approach_quality_band")),
        "code_correctness_reasoning_score": _band_to_score(
            raw.get("code_correctness_reasoning_band")
        ),
        "complexity_analysis_score": _band_to_score(
            raw.get("complexity_analysis_band")
        ),
        "communication_clarity_score": _band_to_score(
            raw.get("communication_clarity_band")
        ),
        "summary": str(raw.get("summary", "")).strip()[:500],
        "strengths": _normalize_improvements(raw.get("strengths")),
        "additional_improvements": _normalize_improvements(
            raw.get("additional_improvements")
        ),
    }


def _band_to_score(value: Any) -> int:
    if isinstance(value, str):
        band = value.strip().lower()
        if band in BAND_SCORES:
            return BAND_SCORES[band]
    return BAND_SCORES["fair"]


def _normalize_improvements(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    normalized: list[str] = []
    for item in value:
        text = str(item).strip()
        if text:
            normalized.append(text[:220])
    return normalized[:5]


def generate_failed_submission_guidance(
    recent_messages: list[ChatTurn],
    failure_context: dict[str, Any],
) -> dict[str, Any]:
    client = _build_client()
    transcript = "\n".join(
        f"{turn['role']}: {turn['content']}"
        for turn in recent_messages[-6:]
        if turn.get("role") and turn.get("content")
    )
    failure_summary = _summarize_failure_context(failure_context)
    contents = (
        "Conversation so far:\\n"
        f"{transcript or 'No prior messages yet.'}\\n\\n"
        "Most recent automated test failure:\\n"
        f"{failure_summary}"
    )
    if not client:
        return _fallback_failure_guidance(failure_summary)
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL_CHAT,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are an encouraging technical interviewer. "
                    "Tests failed for the candidate's latest submission. "
                    "Produce a short coaching response (<=90 words) "
                    "that cites the failing test case and offers 1-2 concrete debugging steps. "
                    "Return strict JSON with fields assistant_message and next_steps."
                ),
                response_mime_type="application/json",
                response_schema=SubmissionFailureResponse,
                temperature=0.2,
            ),
        )
        parsed = cast(SubmissionFailureResponse | None, response.parsed)
        if parsed is None:
            raise ValueError("Missing parsed failure guidance")
        _log_usage(response, "interview_failure_guidance")
        return parsed.model_dump()
    except Exception as exc:
        logger.exception("Gemini failure guidance error")
        if _is_quota_error(exc):
            raise InterviewAIError(
                "AI quota exceeded. Please check your Gemini billing/quota and try again."
            ) from exc
        if _is_strict_mode():
            raise InterviewAIError(
                f"Gemini failure guidance failed: {type(exc).__name__}"
            ) from exc
        return _fallback_failure_guidance(failure_summary)


def _fallback_failure_guidance(failure_summary: str) -> dict[str, Any]:
    return {
        "assistant_message": (
            "Your latest submission is still failing the automated tests. "
            f"Here's what we know: {failure_summary}. "
            "Please revisit your code, add a local print or dry run for that scenario, "
            "and submit again once it passes."
        ),
        "next_steps": [
            "Reproduce the failing test locally and inspect intermediate values.",
            "Update the code to handle that scenario, then resubmit to rerun tests.",
        ],
    }


def _summarize_failure_context(failure_context: dict[str, Any]) -> str:
    index = failure_context.get("case_index")
    total = failure_context.get("case_total")
    params = failure_context.get("params")
    expected = failure_context.get("expected_output")
    error_message = failure_context.get("error_message") or "Runtime failure"
    pieces = []
    if index and total:
        pieces.append(f"Test case #{index} of {total}")
    if params is not None:
        pieces.append(f"Input: {params}")
    if expected is not None:
        pieces.append(f"Expected: {expected}")
    pieces.append(f"Observed error: {error_message}")
    return "; ".join(str(part) for part in pieces if part)
