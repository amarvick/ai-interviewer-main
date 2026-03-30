import type { InterviewCompletionResponse } from "@/types/interview";
import type { FeedbackPanelState } from "@/features/interview/hooks/useFeedbackPanelState";
import ScoreCard from "@/features/interview/components/ScoreCard/ScoreCard";

interface FeedbackPanelProps
  extends Pick<
    FeedbackPanelState,
    | "rubricRows"
    | "feedbackSummary"
    | "keyOpportunities"
    | "additionalOnly"
    | "showAdditional"
  > {
  completionResult: InterviewCompletionResponse | null;
  isLoading: boolean;
  finalScore: number | null;
  didPass: boolean | null;
}

export default function FeedbackPanel({
  completionResult,
  isLoading,
  rubricRows,
  feedbackSummary,
  finalScore,
  didPass,
  keyOpportunities,
  additionalOnly,
  showAdditional,
}: FeedbackPanelProps) {
  if (isLoading) {
    return (
      <div className="feedback-loading" role="status" aria-live="polite">
        <span className="feedback-spinner" aria-hidden="true" />
        <span>Generating feedback...</span>
      </div>
    );
  }

  return (
    <>
      {completionResult && (
        <ScoreCard finalScore={finalScore} didPass={didPass} />
      )}
      <h3>Rubric</h3>
      {rubricRows.length === 0 && (
        <p className="interview-chat-empty">
          Feedback will appear here once the interview has enough signal.
        </p>
      )}
      {rubricRows.length > 0 && (
        <div className="rubric-table">
          {rubricRows.map((row) => (
            <div key={row.label} className="rubric-row">
              <span>{row.label}</span>
              <span>{row.value.toFixed(2)} / 10.00</span>
            </div>
          ))}
        </div>
      )}
      {completionResult && (
        <div className="feedback-block">
          <h4>Summary</h4>
          {feedbackSummary ? (
            <p className="feedback-summary-text">{feedbackSummary}</p>
          ) : (
            <p className="feedback-summary-text">
              Highlights and key opportunities are summarized below.
            </p>
          )}
          {completionResult.strengths.length > 0 && (
            <>
              <h5>Highlights</h5>
              <ul className="feedback-list">
                {completionResult.strengths.map((item) => (
                  <li key={`strength-${item}`}>{item}</li>
                ))}
              </ul>
            </>
          )}
          {keyOpportunities.length > 0 && (
            <>
              <h5>Key Opportunities</h5>
              <ul className="feedback-list">
                {keyOpportunities.map((item) => (
                  <li key={`gap-${item}`}>{item}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
      {showAdditional && (
        <div className="feedback-block">
          <h4>Additional Improvements</h4>
          <ul className="feedback-list">
            {additionalOnly.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      )}
    </>
  );
}
