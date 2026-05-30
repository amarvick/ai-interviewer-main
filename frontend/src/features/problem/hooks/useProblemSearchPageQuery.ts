import { useQuery } from "@tanstack/react-query";
import { getProblemSearchPage } from "@/services/api";
import { useDebouncedValue } from "./useDebouncedValue";

interface UseProblemSearchPageQueryOptions {
  problemListId: string;
  searchTerm: string;
  page: number;
  pageSize?: number;
  debounceMs?: number;
}

export function useProblemSearchPageQuery({
  problemListId,
  searchTerm,
  page,
  pageSize = 10,
  debounceMs = 300,
}: UseProblemSearchPageQueryOptions) {
  const debouncedSearchTerm = useDebouncedValue(searchTerm, debounceMs);

  return useQuery({
    queryKey: [
      "problem-search-page",
      problemListId,
      debouncedSearchTerm,
      page,
      pageSize,
    ],
    queryFn: ({ signal }) =>
      getProblemSearchPage(
        {
          problemListId,
          search: debouncedSearchTerm,
          page,
          pageSize,
        },
        signal
      ),
    enabled: Boolean(problemListId),
    placeholderData: (previousData) => previousData,
  });
}
