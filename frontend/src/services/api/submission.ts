import type {
  SubmissionPayload,
  SubmissionResponse,
} from "../../types/submission";
import {
  API_BASE_URL,
  buildAuthHeaders,
  requestJson,
} from "./api";

export async function runSubmission(
  payload: SubmissionPayload
): Promise<SubmissionResponse> {
  return requestJson<SubmissionResponse>(`${API_BASE_URL}/submission/submit`, {
    method: "POST",
    headers: buildAuthHeaders({
      "Content-Type": "application/json",
    }),
    body: JSON.stringify(payload),
  });
}

export async function getSubmissions(
  problemId: string,
  signal?: AbortSignal
): Promise<SubmissionResponse[]> {
  return requestJson<SubmissionResponse[]>(
    `${API_BASE_URL}/submissions?problem_id=${encodeURIComponent(problemId)}`,
    {
      headers: buildAuthHeaders(),
      signal,
    }
  );
}
