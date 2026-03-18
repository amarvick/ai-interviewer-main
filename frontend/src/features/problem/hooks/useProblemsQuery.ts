import { useQuery } from "@tanstack/react-query";
import { getProblemsByProblemListId } from "@/services/api";

export function useProblemsQuery(problemListId: string) {
  return useQuery({
    queryKey: ["problems", problemListId],
    queryFn: ({ signal }) => getProblemsByProblemListId(problemListId, signal),
    enabled: Boolean(problemListId),
  });
}
