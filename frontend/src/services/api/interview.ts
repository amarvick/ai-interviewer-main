import type {
  InterviewCompletionResponse,
  InterviewMessagePayload,
  InterviewSessionDetailResponse,
  InterviewSessionResponse,
  StartInterviewSessionPayload,
} from "../../types/interview";
import {
  API_BASE_URL,
  buildAuthHeaders,
  requestJson,
} from "./api";

export async function startInterviewSession(
  payload: StartInterviewSessionPayload
): Promise<InterviewSessionResponse> {
  return requestJson<InterviewSessionResponse>(
    `${API_BASE_URL}/interview/session/start`,
    {
      method: "POST",
      headers: buildAuthHeaders({
        "Content-Type": "application/json",
      }),
      body: JSON.stringify(payload),
    }
  );
}

export async function getInterviewSession(
  sessionId: string
): Promise<InterviewSessionDetailResponse> {
  return requestJson<InterviewSessionDetailResponse>(
    `${API_BASE_URL}/interview/session/${sessionId}`,
    {
      headers: buildAuthHeaders(),
    }
  );
}

export async function postInterviewMessage(
  sessionId: string,
  payload: InterviewMessagePayload
): Promise<InterviewSessionDetailResponse> {
  return requestJson<InterviewSessionDetailResponse>(
    `${API_BASE_URL}/interview/session/${sessionId}/message`,
    {
      method: "POST",
      headers: buildAuthHeaders({
        "Content-Type": "application/json",
      }),
      body: JSON.stringify(payload),
    }
  );
}

export async function completeInterviewSession(
  sessionId: string,
  finalScore?: number
): Promise<InterviewCompletionResponse> {
  return requestJson<InterviewCompletionResponse>(
    `${API_BASE_URL}/interview/session/${sessionId}/complete`,
    {
      method: "POST",
      headers: buildAuthHeaders({
        "Content-Type": "application/json",
      }),
      body: JSON.stringify({ final_score: finalScore ?? null }),
    }
  );
}
