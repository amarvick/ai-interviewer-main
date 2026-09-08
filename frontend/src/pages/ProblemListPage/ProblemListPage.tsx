import { useState } from "react";
import { useParams } from "react-router-dom";
import { useProblemSearchPageQuery } from "@/features/problem/hooks/useProblemSearchPageQuery";
import ProblemGrid from "../../components/ProblemGrid/ProblemGrid";
import "./ProblemListPage.css";

const PAGE_SIZE = 10;

export default function ProblemListPage() {
  const { id } = useParams();
  const [searchTerm, setSearchTerm] = useState("");
  const [page, setPage] = useState(1);

  const { data, isLoading, isError, error } = useProblemSearchPageQuery({
    problemListId: id ?? "",
    searchTerm,
    page,
    pageSize: PAGE_SIZE,
  });

  const clearSearch = () => {
    setSearchTerm("");
    setPage(1);
  };

  return (
    <section className="problem-list-section">
      <h1>{data?.name ?? "Problem List"}</h1>
      {isLoading && (
        <p className="status-line" role="status" aria-live="polite">
          Loading problems...
        </p>
      )}
      {isError && (
        <p className="status-line error" role="alert">
          {(error as Error).message || "Request failed."}
        </p>
      )}
      {!isLoading && !isError && data && (
        <>
          <div className="problem-filters" aria-label="Problem filters">
            <div className="filter-group full-width">
              <label htmlFor="problem-search">Search problems</label>
              <input
                id="problem-search"
                type="search"
                value={searchTerm}
                placeholder="Search by title, category, or difficulty..."
                onChange={(event) => {
                  setSearchTerm(event.target.value);
                  setPage(1);
                }}
              />
            </div>

            {searchTerm.trim().length > 0 && (
              <button
                type="button"
                className="filter-reset"
                onClick={clearSearch}
              >
                Clear search
              </button>
            )}
          </div>

          {data.problems.length > 0 ? (
            <>
              <ProblemGrid problems={data.problems} />
              <div className="pagination-controls" aria-label="Problem pages">
                <button
                  type="button"
                  disabled={!data.has_previous_page}
                  onClick={() => setPage((currentPage) => currentPage - 1)}
                >
                  Previous
                </button>
                <span>
                  Page {data.page} of {data.total_pages || 1}
                </span>
                <button
                  type="button"
                  disabled={!data.has_next_page}
                  onClick={() => setPage((currentPage) => currentPage + 1)}
                >
                  Next
                </button>
              </div>
            </>
          ) : (
            <p className="status-line" role="status" aria-live="polite">
              No problems match the current search.
            </p>
          )}
        </>
      )}
    </section>
  );
}
