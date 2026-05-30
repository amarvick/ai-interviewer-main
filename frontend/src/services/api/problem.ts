import type {
  Problem,
  ProblemList,
  ProblemSearchPageParams,
  ProblemSearchPageResponse,
} from "../../types/problem";
import { API_BASE_URL, buildAuthHeaders, requestJson } from "./api";

export async function getProblemLists(
  signal?: AbortSignal
): Promise<ProblemList[]> {
  return requestJson<ProblemList[]>(`${API_BASE_URL}/problem-lists`, {
    signal,
  });
}

export async function getProblemSearchPage(
  {
    problemListId,
    search = "",
    page = 1,
    pageSize = 10,
  }: ProblemSearchPageParams,
  signal: AbortSignal
): Promise<ProblemSearchPageResponse> {
  const params = new URLSearchParams({
    search,
    page: String(page),
    page_size: String(pageSize),
  });

  return requestJson<ProblemSearchPageResponse>(
    `${API_BASE_URL}/problems/${problemListId}/search?${params.toString()}`,
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
  return requestJson<Problem>(`${API_BASE_URL}/problem/${problemSlug}`, {
    signal,
  });
}
