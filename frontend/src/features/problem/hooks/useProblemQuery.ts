import { useQuery } from "@tanstack/react-query";
import { getProblemById } from "@/services/api";

export function useProblemQuery(problemId: string) {
  return useQuery({
    queryKey: ["problem", problemId],
    queryFn: ({ signal }) => getProblemById(problemId, signal),
    enabled: Boolean(problemId),
  });
}
