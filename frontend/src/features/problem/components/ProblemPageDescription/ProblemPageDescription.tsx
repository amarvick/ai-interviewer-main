import { useMemo } from "react";
import DOMPurify from "dompurify";
import { marked } from "marked";
import type { Problem } from "@/types/problem";
import styles from "./ProblemPageDescription.module.css";

interface ProblemPageDescriptionProps {
  problem: Problem;
}

export default function ProblemPageDescription({
  problem,
}: ProblemPageDescriptionProps) {
  const descriptionHtml = useMemo(() => {
    const raw = marked.parse(problem.description || "", {
      breaks: true,
      gfm: true,
    }) as string;
    return DOMPurify.sanitize(raw);
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
        <div
          className={styles.descriptionContent}
          dangerouslySetInnerHTML={{ __html: descriptionHtml }}
        />
      </section>
    </article>
  );
}
