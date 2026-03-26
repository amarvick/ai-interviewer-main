import type {
  Problem,
  ProblemList,
  ProblemListProblemsResponse,
} from "../../types/problem";
import {
  API_BASE_URL,
  buildAuthHeaders,
  requestJson,
} from "./api";

export async function getProblemLists(signal?: AbortSignal): Promise<ProblemList[]> {
  return requestJson<ProblemList[]>(`${API_BASE_URL}/problem-lists`, { signal });
}

export async function getProblemsByProblemListId(
  problemListId: string,
  signal?: AbortSignal
): Promise<ProblemListProblemsResponse> {
  return requestJson<ProblemListProblemsResponse>(
    `${API_BASE_URL}/problems/${problemListId}`,
    {
      headers: buildAuthHeaders(),
      signal,
    }
  );
}

export async function getProblemBySlug(
  problemSlug: string,
  signal?: AbortSignal
): Promise<Problem> {
  return requestJson<Problem>(`${API_BASE_URL}/problem/${problemSlug}`, { signal });
}
