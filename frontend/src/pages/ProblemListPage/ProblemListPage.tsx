import { useParams } from "react-router-dom";
import { useProblemsQuery } from "@/features/problem/hooks/useProblemsQuery";
import ProblemGrid from "../../components/ProblemGrid/ProblemGrid";
import "./ProblemListPage.css";

export default function ProblemListPage() {
  const { id } = useParams();
  const { data, isLoading, isError, error } = useProblemsQuery(id ?? "");

  /* TODO -- create loading spinner */
  return (
    <section className="problem-list-section">
      <h1>{data?.name ?? "Problem List"}</h1>
      {isLoading && (
        <p className="status-line" role="status" aria-live="polite">
          Loading problem lists...
        </p>
      )}
      {isError && (
        <p className="status-line error" role="alert">
          {(error as Error).message || "Request failed."}
        </p>
      )}
      {!isLoading && !isError && data && data.problems.length > 0 && (
        <ProblemGrid problems={data.problems} />
      )}
      {!isLoading && !isError && data?.problems.length === 0 && (
        <p className="status-line" role="status" aria-live="polite">
          No problem lists found yet.
        </p>
      )}
    </section>
  );
}
