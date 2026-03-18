import { useMemo } from "react";
import DOMPurify from "dompurify";
import { marked } from "marked";
import type { Problem } from "../../types/problem";
import "./ProblemPageDescription.css";

interface ProblemPageDescriptionProps {
  problem: Problem;
}

export default function ProblemPageDescription({
  problem,
}: ProblemPageDescriptionProps) {
  const descriptionHtml = useMemo(() => {
    const raw = marked.parse(problem.description || "", {
      breaks: true,
      mangle: false,
      headerIds: false,
    });
    return DOMPurify.sanitize(raw);
  }, [problem.description]);

  return (
    <article className="problem-panel" aria-labelledby="problem-title">
      <header className="problem-panel-header">
        <h1 id="problem-title">{problem.title}</h1>
        <p className="problem-meta">
          <span>{problem.category}</span>
          <span aria-hidden="true"> • </span>
          <span>{problem.difficulty}</span>
        </p>
      </header>

      <section className="problem-description">
        <h2>Description</h2>
        <div
          className="problem-description-content"
          dangerouslySetInnerHTML={{ __html: descriptionHtml }}
        />
      </section>
    </article>
  );
}
