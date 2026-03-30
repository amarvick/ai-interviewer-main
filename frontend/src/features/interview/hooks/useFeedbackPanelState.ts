import { useMemo } from "react";
import type {
  InterviewCompletionResponse,
  InterviewEvaluationResponse,
} from "@/types/interview";
import {
  buildNitpicks,
  summarizeRubric,
  extractLatestSummary,
  extractAiAdditionalImprovements,
} from "@/features/interview/utils/interview";

export interface FeedbackPanelState {
  rubricRows: ReturnType<typeof summarizeRubric>;
  nitpicks: string[];
  feedbackSummary: string | null;
  finalScore: number | null;
  didPass: boolean | null;
  keyOpportunities: string[];
  additionalOnly: string[];
  showAdditional: boolean;
}

export function useFeedbackPanelState(
  evaluations: InterviewEvaluationResponse[],
  completionResult: InterviewCompletionResponse | null
): FeedbackPanelState {
  const rubricRows = useMemo(
    () => summarizeRubric(evaluations),
    [evaluations]
  );

  const aiAdditional = useMemo(
    () => extractAiAdditionalImprovements(evaluations),
    [evaluations]
  );

  const nitpicks = useMemo(
    () =>
      aiAdditional.length > 0
        ? aiAdditional
        : buildNitpicks(rubricRows, completionResult),
    [aiAdditional, completionResult, rubricRows]
  );

  const feedbackSummary = useMemo(
    () => extractLatestSummary(evaluations),
    [evaluations]
  );

  const finalScore = completionResult?.final_score ?? null;
  const didPass = finalScore !== null ? finalScore >= 30 : null;
  const keyOpportunities = completionResult?.gaps ?? [];
  const additionalOnly = nitpicks.filter(
    (item) => !keyOpportunities.includes(item)
  );
  const showAdditional = additionalOnly.length > 0;

  return {
    rubricRows,
    nitpicks,
    feedbackSummary,
    finalScore,
    didPass,
    keyOpportunities,
    additionalOnly,
    showAdditional,
  };
}
