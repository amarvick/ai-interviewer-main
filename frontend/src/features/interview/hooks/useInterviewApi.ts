import { useCallback, useEffect, useMemo, useState } from "react";
import type { Problem } from "@/types/problem";
import type {
  InterviewCompletionResponse,
  InterviewEvaluationResponse,
  InterviewSessionStatus,
  InterviewSessionDetailResponse,
} from "@/types/interview";
import {
  completeInterviewSession,
  getInterviewSession,
  postInterviewMessage,
  runSubmission,
  startInterviewSession,
} from "@/services/api";
import type { ChatMessage } from "@/features/interview/utils/interview";
import { toChatHistory } from "@/features/interview/utils/interview";
import type { Language } from "@/types/language";
import {
  adaptCompletionResponse,
  adaptSessionDetail,
} from "@/features/interview/adapters/sessionAdapter";

interface UseInterviewApiParams {
  problem: Problem;
}

export interface InterviewTransportState {
  sessionId: string | null;
  status: InterviewSessionStatus;
  canSubmit: boolean;
  messages: ChatMessage[];
  evaluations: InterviewEvaluationResponse[];
  completionResult: InterviewCompletionResponse | null;
  isSending: boolean;
  isSubmittingCode: boolean;
  isLoadingFeedback: boolean;
  error: string | null;
}

interface SubmitResult {
  summary: string;
}

export interface UseInterviewApiResult extends InterviewTransportState {
  sendChatMessage: (content: string, currentCode: string) => Promise<void>;
  submitSolution: (
    code: string,
    language: Language
  ) => Promise<SubmitResult | null>;
}

const INITIAL_STATE: InterviewTransportState = {
  sessionId: null,
  status: "ACTIVE",
  canSubmit: false,
  messages: [],
  evaluations: [],
  completionResult: null,
  isSending: false,
  isSubmittingCode: false,
  isLoadingFeedback: false,
  error: null,
};

export function useInterviewApi({
  problem,
}: UseInterviewApiParams): UseInterviewApiResult {
  const [state, setState] = useState<InterviewTransportState>(INITIAL_STATE);

  const applySessionDetail = useCallback(
    (detail: InterviewSessionDetailResponse) => {
      const adapted = adaptSessionDetail(detail);
      setState((prev) => ({
        ...prev,
        sessionId: adapted.id,
        status: adapted.status,
        evaluations: adapted.evaluations,
        messages: adapted.messages,
        canSubmit: prev.canSubmit || adapted.canSubmit,
      }));
    },
    []
  );

  useEffect(() => {
    let isMounted = true;
    const initialize = async () => {
      setState(() => ({
        ...INITIAL_STATE,
      }));

      try {
        const started = await startInterviewSession({ problem_id: problem.id });
        const detail = await getInterviewSession(started.id);
        if (isMounted) {
          applySessionDetail(detail);
        }
      } catch (error) {
        if (!isMounted) {
          return;
        }
        const message =
          error instanceof Error
            ? error.message
            : "Failed to start interview session.";
        setState((prev) => ({ ...prev, error: message }));
      }
    };

    void initialize();

    return () => {
      isMounted = false;
    };
  }, [applySessionDetail, problem.id]);

  useEffect(() => {
    if (
      state.status !== "COMPLETED" ||
      !state.sessionId ||
      state.completionResult ||
      state.isLoadingFeedback
    ) {
      return;
    }

    let isMounted = true;
    setState((prev) => ({ ...prev, isLoadingFeedback: true }));

    const hydrate = async () => {
      try {
        const result = await completeInterviewSession(state.sessionId!);
        const normalized = adaptCompletionResponse(result);
        const detail = await getInterviewSession(state.sessionId!);
        if (!isMounted) {
          return;
        }
        applySessionDetail(detail);
        setState((prev) => ({
          ...prev,
          completionResult: normalized,
        }));
      } catch {
        // swallow to keep chat working
      } finally {
        if (isMounted) {
          setState((prev) => ({ ...prev, isLoadingFeedback: false }));
        }
      }
    };

    void hydrate();

    return () => {
      isMounted = false;
    };
  }, [
    applySessionDetail,
    state.completionResult,
    state.sessionId,
    state.status,
  ]);

  const sendChatMessage = useCallback(
    async (content: string, currentCode: string) => {
      if (!state.sessionId) {
        return;
      }
      const trimmed = content.trim();
      if (!trimmed) {
        return;
      }

      const optimisticMessage: ChatMessage = {
        id: `optimistic-${Date.now()}`,
        role: "you",
        content: trimmed,
        createdAt: Date.now(),
      };
      const nextMessages = [...state.messages, optimisticMessage];
      setState((prev) => ({
        ...prev,
        messages: nextMessages,
        isSending: true,
        error: null,
      }));
      try {
        const detail = await postInterviewMessage(state.sessionId, {
          content: trimmed,
          role: "user",
          has_submission: false,
          current_code: currentCode,
          chat_history: toChatHistory(nextMessages),
        });
        applySessionDetail(detail);
      } catch (error) {
        const message =
          error instanceof Error ? error.message : "Failed to send message.";
        setState((prev) => ({
          ...prev,
          error: message,
          messages: prev.messages.filter(
            (message) => message.id !== optimisticMessage.id
          ),
        }));
        throw new Error(message);
      } finally {
        setState((prev) => ({ ...prev, isSending: false }));
      }
    },
    [applySessionDetail, state.messages, state.sessionId]
  );

  const submitSolution = useCallback(
    async (code: string, language: Language): Promise<SubmitResult | null> => {
      if (!state.sessionId) {
        return null;
      }
      setState((prev) => ({ ...prev, isSubmittingCode: true, error: null }));
      try {
        const submission = await runSubmission({
          problem_id: problem.id,
          code_submitted: code,
          language,
        });

        const summary =
          submission.result === "pass"
            ? `I submitted my ${language} solution and all tests passed.`
            : `I submitted my ${language} solution and it failed. Error: ${
                submission.error ?? "Unknown failure"
              }`;

        const optimisticMessage: ChatMessage = {
          id: `submission-${Date.now()}`,
          role: "you",
          content: summary,
          createdAt: Date.now(),
        };

        const nextMessages = [...state.messages, optimisticMessage];
        setState((prev) => ({
          ...prev,
          messages: nextMessages,
        }));

        const detail = await postInterviewMessage(state.sessionId, {
          content: summary,
          role: "user",
          has_submission: true,
          current_code: code,
          chat_history: toChatHistory(nextMessages),
        });
        applySessionDetail(detail);
        return { summary };
      } catch (error) {
        const message =
          error instanceof Error ? error.message : "Failed to submit code.";
        setState((prev) => ({ ...prev, error: message }));
        return null;
      } finally {
        setState((prev) => ({ ...prev, isSubmittingCode: false }));
      }
    },
    [applySessionDetail, problem.id, state.messages, state.sessionId]
  );

  const mergedState = useMemo(
    () => ({
      ...state,
      sendChatMessage,
      submitSolution,
    }),
    [sendChatMessage, state, submitSolution]
  );

  return mergedState;
}
