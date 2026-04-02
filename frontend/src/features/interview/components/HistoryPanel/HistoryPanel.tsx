import type { InterviewEvaluationResponse } from "@/types/interview";

interface HistoryPanelProps {
  evaluations: InterviewEvaluationResponse[];
}

function formatTimestamp(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toLocaleString(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

export default function HistoryPanel({ evaluations }: HistoryPanelProps) {
  if (!evaluations.length) {
    return (
      <p className="interview-chat-empty">
        Once you complete an interview, past evaluations will appear here.
      </p>
    );
  }

  const ordered = [...evaluations].sort(
    (a, b) =>
      new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  );

  return (
    <div className="history-panel">
      {ordered.map((evaluation) => {
        const summary =
          typeof evaluation.summary === "string" && evaluation.summary.length
            ? evaluation.summary
            : "No summary provided for this evaluation.";
        const rubric = evaluation.rubric_json ?? {};
        const additional = Array.isArray(rubric.additional_improvements)
          ? (rubric.additional_improvements as string[])
          : [];
        const strengths = Array.isArray(rubric.strengths)
          ? (rubric.strengths as string[])
          : [];
        return (
          <details key={evaluation.id} className="history-card">
            <summary>
              <div>
                <span className="history-card-title">
                  {formatTimestamp(evaluation.created_at)}
                </span>
                <span className="history-card-subtitle">
                  Stage: {evaluation.stage}
                </span>
              </div>
              <span className="history-card-score">
                Total: {evaluation.total_score.toFixed(2)} / 50
              </span>
            </summary>
            <div className="history-card-body">
              <p className="history-card-summary">{summary}</p>
              <div className="history-card-grid">
                <dl>
                  <dt>Problem Understanding</dt>
                  <dd>{evaluation.problem_understanding_score.toFixed(2)}</dd>
                  <dt>Approach Quality</dt>
                  <dd>{evaluation.approach_quality_score.toFixed(2)}</dd>
                  <dt>Correctness Reasoning</dt>
                  <dd>{evaluation.code_correctness_reasoning_score.toFixed(2)}</dd>
                  <dt>Complexity Analysis</dt>
                  <dd>{evaluation.complexity_analysis_score.toFixed(2)}</dd>
                  <dt>Communication Clarity</dt>
                  <dd>{evaluation.communication_clarity_score.toFixed(2)}</dd>
                </dl>
                <div>
                  {strengths.length > 0 && (
                    <>
                      <h5>Highlights</h5>
                      <ul>
                        {strengths.map((item, index) => (
                          <li key={`${evaluation.id}-strength-${index}`}>{item}</li>
                        ))}
                      </ul>
                    </>
                  )}
                  {additional.length > 0 && (
                    <>
                      <h5>Improvements</h5>
                      <ul>
                        {additional.map((item, index) => (
                          <li key={`${evaluation.id}-improvement-${index}`}>
                            {item}
                          </li>
                        ))}
                      </ul>
                    </>
                  )}
                </div>
              </div>
            </div>
          </details>
        );
      })}
    </div>
  );
}
