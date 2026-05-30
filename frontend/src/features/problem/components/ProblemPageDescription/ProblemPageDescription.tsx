import { useMemo } from "react";
import { marked } from "marked";
import { renderBlockToken } from "../../utils/problemDescription";
import type { Problem } from "@/types/problem";
import styles from "./ProblemPageDescription.module.css";

interface ProblemPageDescriptionProps {
  problem: Problem;
}

export default function ProblemPageDescription({
  problem,
}: ProblemPageDescriptionProps) {
  const descriptionTokens = useMemo(() => {
    return marked.lexer(problem.description || "", {
      breaks: true,
      gfm: true,
    });
  }, [problem.description]);

  return (
    <article className={styles.problemPanel} aria-labelledby="problem-title">
      <header className={styles.problemPanelHeader}>
        <h1 id="problem-title">{problem.title}</h1>
        <p className={styles.problemMeta}>
          <span>{problem.category}</span>
          <span aria-hidden="true"> • </span>
          <span>{problem.difficulty}</span>
        </p>
      </header>

      <section className={styles.descriptionSection}>
        <h2 className={styles.descriptionHeading}>Description</h2>
        <div className={styles.descriptionContent}>
          {descriptionTokens.map((token, index) =>
            renderBlockToken(token, index)
          )}
        </div>
      </section>
    </article>
  );
}
