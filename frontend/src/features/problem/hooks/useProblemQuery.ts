import { useQuery } from "@tanstack/react-query";
import { getProblemBySlug } from "@/services/api";

export function useProblemQuery(problemSlug: string) {
  return useQuery({
    queryKey: ["problem", problemSlug],
    queryFn: ({ signal }) => getProblemBySlug(problemSlug, signal),
    enabled: Boolean(problemSlug),
  });
}
