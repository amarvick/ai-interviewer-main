import { useMemo, useState } from "react";
import type { TestCase } from "@/types/testcase";
import type { SubmissionResponse } from "@/types/submission";
import styles from "./ProblemPageTerminal.module.css";

type TestCaseStatus = "pending" | "pass" | "fail";

interface ProblemPageTerminalProps {
  testCases: TestCase[];
  testCaseStatuses: Record<string, TestCaseStatus>;
  submissions: SubmissionResponse[];
  hasSubmittedInSession: boolean;
  sessionErrors: string[];
  isSubmitting?: boolean;
}

function prettyJson(value: unknown): string {
  try {
    return JSON.stringify(value);
  } catch {
    return String(value);
  }
}

export default function ProblemPageTerminal({
  testCases,
  testCaseStatuses,
  submissions,
  hasSubmittedInSession,
  sessionErrors,
  isSubmitting = false,
}: ProblemPageTerminalProps) {
  const [activeTab, setActiveTab] = useState<"results" | "submissions">(
    "results"
  );
  const orderedSubmissions = useMemo(
    () =>
      [...submissions].sort((a, b) => {
        const aTime = a.created_at ? new Date(a.created_at).getTime() : 0;
        const bTime = b.created_at ? new Date(b.created_at).getTime() : 0;
        return bTime - aTime;
      }),
    [submissions]
  );

  return (
    <section
      className={styles.terminalPanel}
      aria-label="Submission and results panel"
    >
      <header className={styles.terminalHeader}>
        <div className={styles.terminalTabs}>
          <button
            type="button"
            className={
              activeTab === "results"
                ? `${styles.tabButton} ${styles.tabButtonActive}`
                : styles.tabButton
            }
            onClick={() => setActiveTab("results")}
            disabled={isSubmitting}
          >
            Test Results
          </button>
          <button
            type="button"
            className={
              activeTab === "submissions"
                ? `${styles.tabButton} ${styles.tabButtonActive}`
                : styles.tabButton
            }
            onClick={() => setActiveTab("submissions")}
            disabled={isSubmitting}
          >
            Submissions
          </button>
        </div>
      </header>

      <div className={styles.terminalOutput}>
        {sessionErrors.length > 0 && (
          <div className={styles.submissionError} role="alert">
            {sessionErrors.map((error, index) => (
              <p key={`${error}-${index}`}>{error}</p>
            ))}
          </div>
        )}
        {activeTab === "results" && (
          <div className={styles.terminalList}>
            {!hasSubmittedInSession && (
              <p className={styles.terminalEmpty}>
                You must submit your code first
              </p>
            )}

            {hasSubmittedInSession &&
              testCases.map((testCase, index) => {
                const status = testCaseStatuses[testCase.id] ?? "pending";
                return (
                  <article key={testCase.id} className={styles.terminalItem}>
                    <div className={styles.terminalItemTitle}>
                      <span
                        className={`${styles.statusDot} ${
                          status === "pass"
                            ? styles.statusPass
                            : status === "fail"
                            ? styles.statusFail
                            : styles.statusPending
                        }`}
                      />
                      <strong>Case {index + 1}</strong>
                    </div>
                    <div className={styles.terminalItemMeta}>
                      <span>Input: {prettyJson(testCase.params)}</span>
                      <span>
                        Expected: {prettyJson(testCase.expected_output)}
                      </span>
                    </div>
                  </article>
                );
              })}
          </div>
        )}

        {activeTab === "submissions" && (
          <div className={styles.terminalList}>
            {orderedSubmissions.map((submission, index) => (
              <article key={submission.id} className={styles.terminalItem}>
                <div className={styles.terminalItemTitle}>
                  <span
                    className={`${styles.statusDot} ${
                      submission.result === "pass"
                        ? styles.statusPass
                        : styles.statusFail
                    }`}
                  />
                  <strong>
                    Submission #{orderedSubmissions.length - index}
                  </strong>
                </div>
                <div className={styles.terminalItemMeta}>
                  <span>
                    Date:{" "}
                    {submission.created_at
                      ? new Date(submission.created_at).toLocaleString()
                      : "Unavailable"}
                  </span>
                  <span>Language: {submission.language}</span>
                  <span>Result: {submission.result.toUpperCase()}</span>
                  <span>
                    Tests: {submission.tests_passed ?? 0} /{" "}
                    {submission.tests_total ?? 0}
                  </span>
                </div>
              </article>
            ))}
            {orderedSubmissions.length === 0 && (
              <p className={styles.terminalEmpty}>No submissions yet.</p>
            )}
          </div>
        )}
      </div>
    </section>
  );
}
