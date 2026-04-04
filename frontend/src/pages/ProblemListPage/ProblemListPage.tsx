import { useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import { useProblemsQuery } from "@/features/problem/hooks/useProblemsQuery";
import ProblemGrid from "../../components/ProblemGrid/ProblemGrid";
import type { Problem } from "@/types/problem";
import "./ProblemListPage.css";

type SortOption =
  | "default"
  | "title_asc"
  | "title_desc"
  | "difficulty_asc"
  | "difficulty_desc";

interface AugmentedProblem {
  problem: Problem;
  index: number;
  difficultyKey: string;
  categoryKey: string;
  searchableText: string;
}

const DIFFICULTY_ORDER: Record<string, number> = {
  easy: 0,
  medium: 1,
  hard: 2,
};

const humanize = (value: string) => {
  if (!value) {
    return "Uncategorized";
  }
  return value
    .split(" ")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1).toLowerCase())
    .join(" ");
};

export default function ProblemListPage() {
  const { id } = useParams();
  const { data, isLoading, isError, error } = useProblemsQuery(id ?? "");
  const [searchTerm, setSearchTerm] = useState("");
  const [difficultyFilters, setDifficultyFilters] = useState<Set<string>>(
    new Set()
  );
  const [categoryFilters, setCategoryFilters] = useState<Set<string>>(
    new Set()
  );
  const [sortOption, setSortOption] = useState<SortOption>("default");
  const [showDifficultyFilters, setShowDifficultyFilters] = useState(false);
  const [showCategoryFilters, setShowCategoryFilters] = useState(false);
  const [showSortMenu, setShowSortMenu] = useState(false);

  const augmentedProblems: AugmentedProblem[] = useMemo(() => {
    if (!data?.problems) {
      return [];
    }
    return data.problems.map((problem, index) => {
      const difficultyKey = String(problem.difficulty ?? "").toLowerCase();
      const categoryKey = String(problem.category ?? "").toLowerCase();
      return {
        problem,
        index,
        difficultyKey,
        categoryKey,
        searchableText: `${problem.title} ${problem.category ?? ""} ${
          problem.difficulty ?? ""
        }`.toLowerCase(),
      };
    });
  }, [data]);

  const difficultyOptions = useMemo(() => {
    const seen = new Set<string>();
    const options: Array<{ value: string; label: string }> = [];
    for (const item of augmentedProblems) {
      if (!seen.has(item.difficultyKey) && item.difficultyKey) {
        seen.add(item.difficultyKey);
        options.push({
          value: item.difficultyKey,
          label: humanize(
            item.problem.difficulty
              ? String(item.problem.difficulty)
              : item.difficultyKey
          ),
        });
      }
    }
    return options.sort((a, b) => {
      const orderDiff =
        (DIFFICULTY_ORDER[a.value] ?? Number.POSITIVE_INFINITY) -
        (DIFFICULTY_ORDER[b.value] ?? Number.POSITIVE_INFINITY);
      if (orderDiff !== 0) {
        return orderDiff;
      }
      return a.label.localeCompare(b.label);
    });
  }, [augmentedProblems]);

  const categoryOptions = useMemo(() => {
    const seen = new Set<string>();
    const options: Array<{ value: string; label: string }> = [];
    for (const item of augmentedProblems) {
      if (!seen.has(item.categoryKey)) {
        seen.add(item.categoryKey);
        options.push({
          value: item.categoryKey,
          label: item.problem.category || "Uncategorized",
        });
      }
    }
    return options.sort((a, b) => a.label.localeCompare(b.label));
  }, [augmentedProblems]);

  const normalizedSearch = searchTerm.trim().toLowerCase();

  const sortOptionsConfig: Array<{ value: SortOption; label: string }> = [
    { value: "default", label: "Default order" },
    { value: "title_asc", label: "Title (A-Z)" },
    { value: "title_desc", label: "Title (Z-A)" },
    { value: "difficulty", label: "Difficulty (Easy → Hard)" },
    { value: "difficulty_desc", label: "Difficulty (Hard → Easy)" },
  ];

  const filteredProblems = useMemo(() => {
    const filtered = augmentedProblems.filter((item) => {
      const matchesDifficulty =
        difficultyFilters.size === 0 ||
        difficultyFilters.has(item.difficultyKey);
      const matchesCategory =
        categoryFilters.size === 0 || categoryFilters.has(item.categoryKey);
      const matchesSearch =
        normalizedSearch.length === 0 ||
        item.searchableText.includes(normalizedSearch);
      return matchesDifficulty && matchesCategory && matchesSearch;
    });

    filtered.sort((a, b) => {
      if (sortOption === "title_asc") {
        return a.problem.title.localeCompare(b.problem.title, undefined, {
          sensitivity: "base",
        });
      }
      if (sortOption === "title_desc") {
        return b.problem.title.localeCompare(a.problem.title, undefined, {
          sensitivity: "base",
        });
      }
      if (sortOption === "difficulty_asc" || sortOption === "difficulty_desc") {
        const orderA =
          DIFFICULTY_ORDER[a.difficultyKey] ?? Number.POSITIVE_INFINITY;
        const orderB =
          DIFFICULTY_ORDER[b.difficultyKey] ?? Number.POSITIVE_INFINITY;
        const diffOrder =
          sortOption === "difficulty_asc" ? orderA - orderB : orderB - orderA;
        if (diffOrder !== 0) {
          return diffOrder;
        }
        return a.problem.title.localeCompare(b.problem.title, undefined, {
          sensitivity: "base",
        });
      }
      return a.index - b.index;
    });

    return filtered.map((item) => item.problem);
  }, [
    augmentedProblems,
    categoryFilters,
    difficultyFilters,
    normalizedSearch,
    sortOption,
  ]);

  const hasActiveFilters =
    normalizedSearch.length > 0 ||
    difficultyFilters.size > 0 ||
    categoryFilters.size > 0 ||
    sortOption !== "default";

  const toggleFilter = (
    value: string,
    setter: React.Dispatch<React.SetStateAction<Set<string>>>
  ) => {
    setter((prev) => {
      const next = new Set(prev);
      if (next.has(value)) {
        next.delete(value);
      } else {
        next.add(value);
      }
      return next;
    });
  };

  const clearFilters = () => {
    setSearchTerm("");
    setDifficultyFilters(new Set());
    setCategoryFilters(new Set());
    setSortOption("default");
    setShowDifficultyFilters(false);
    setShowCategoryFilters(false);
    setShowSortMenu(false);
  };

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
                onChange={(event) => setSearchTerm(event.target.value)}
              />
            </div>

            {difficultyOptions.length > 0 && (
              <div className="filter-group dropdown-group">
                <button
                  type="button"
                  className="dropdown-trigger"
                  aria-haspopup="true"
                  aria-expanded={showDifficultyFilters}
                  onClick={() => setShowDifficultyFilters((prev) => !prev)}
                >
                  Difficulty Filters
                  <span className="dropdown-icon" aria-hidden="true">
                    {showDifficultyFilters ? "▴" : "▾"}
                  </span>
                </button>
                {showDifficultyFilters && (
                  <div className="dropdown-panel" role="menu">
                    <div className="filter-checkboxes column">
                      {difficultyOptions.map((option) => (
                        <label key={option.value}>
                          <input
                            type="checkbox"
                            checked={difficultyFilters.has(option.value)}
                            onChange={() =>
                              toggleFilter(option.value, setDifficultyFilters)
                            }
                          />
                          {option.label}
                        </label>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {categoryOptions.length > 0 && (
              <div className="filter-group dropdown-group">
                <button
                  type="button"
                  className="dropdown-trigger"
                  aria-haspopup="true"
                  aria-expanded={showCategoryFilters}
                  onClick={() => setShowCategoryFilters((prev) => !prev)}
                >
                  Category Filters
                  <span className="dropdown-icon" aria-hidden="true">
                    {showCategoryFilters ? "▴" : "▾"}
                  </span>
                </button>
                {showCategoryFilters && (
                  <div className="dropdown-panel" role="menu">
                    <div className="filter-checkboxes column">
                      {categoryOptions.map((option) => (
                        <label key={option.value || "uncategorized"}>
                          <input
                            type="checkbox"
                            checked={categoryFilters.has(option.value)}
                            onChange={() =>
                              toggleFilter(option.value, setCategoryFilters)
                            }
                          />
                          {option.label || "Uncategorized"}
                        </label>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            <div className="filter-group dropdown-group sort-group">
              <span className="filter-group-label">Sort Order</span>
              <button
                type="button"
                className="dropdown-trigger"
                aria-haspopup="true"
                aria-expanded={showSortMenu}
                onClick={() => setShowSortMenu((prev) => !prev)}
              >
                <span className="dropdown-value">
                  {sortOptionsConfig.find((option) => option.value === sortOption)
                    ?.label ?? "Default order"}
                </span>
                <span className="dropdown-icon" aria-hidden="true">
                  {showSortMenu ? "▴" : "▾"}
                </span>
              </button>
              {showSortMenu && (
                <div className="dropdown-panel" role="menu">
                  <div className="filter-checkboxes column">
                    {sortOptionsConfig.map((option) => (
                      <label key={option.value}>
                        <input
                          type="radio"
                          name="sort-options"
                          value={option.value}
                          checked={sortOption === option.value}
                          onChange={() => {
                            setSortOption(option.value);
                            setShowSortMenu(false);
                          }}
                        />
                        {option.label}
                      </label>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {hasActiveFilters && (
              <button
                type="button"
                className="filter-reset"
                onClick={clearFilters}
              >
                Clear filters
              </button>
            )}
          </div>

          <div className="problem-filter-summary">
            Showing{" "}
            <strong>
              {filteredProblems.length} / {data.problems.length}
            </strong>{" "}
            problems
          </div>

          {filteredProblems.length > 0 ? (
            <ProblemGrid problems={filteredProblems} />
          ) : (
            <p className="status-line" role="status" aria-live="polite">
              No problems match the current filters.
            </p>
          )}
        </>
      )}
      {!isLoading && !isError && data?.problems.length === 0 && (
        <p className="status-line" role="status" aria-live="polite">
          No problem lists found yet.
        </p>
      )}
    </section>
  );
}
