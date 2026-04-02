import { useCallback, useEffect, useMemo, useState } from "react";
import type { KeyboardEvent } from "react";
import type { Problem } from "@/types/problem";
import {
  DEFAULT_LANGUAGE,
  isLanguage,
  type Language,
} from "@/types/language";
import { useInterviewApi } from "@/features/interview/hooks/useInterviewApi";
import {
  useFeedbackPanelState,
  type FeedbackPanelState,
} from "@/features/interview/hooks/useFeedbackPanelState";
import type { ChatMessage } from "@/features/interview/utils/interview";
import type {
  InterviewCompletionResponse,
  InterviewEvaluationResponse,
} from "@/types/interview";

type InterviewPanelTab = "chat" | "feedback" | "history";

export interface UseInterviewSessionResult {
  languageOptions: Language[];
  selectedLanguage: Language;
  code: string;
  draftMessage: string;
  messages: ChatMessage[];
  sessionStatus: "ACTIVE" | "COMPLETED" | "ABANDONED";
  canSubmit: boolean;
  activeTab: InterviewPanelTab;
  evaluations: InterviewEvaluationResponse[];
  completionResult: InterviewCompletionResponse | null;
  isSending: boolean;
  isSubmittingCode: boolean;
  isLoadingFeedback: boolean;
  error: string | null;
  rubricRows: FeedbackPanelState["rubricRows"];
  nitpicks: string[];
  feedbackSummary: string | null;
  finalScore: number | null;
  didPass: boolean | null;
  hasSession: boolean;
  setDraftMessage: (value: string) => void;
  setActiveTab: (tab: InterviewPanelTab) => void;
  handleLanguageChange: (lang: Language) => void;
  updateCode: (value: string | undefined) => void;
  handleSend: () => Promise<void>;
  handleSubmitCode: () => Promise<void>;
  handleDraftKeyDown: (event: KeyboardEvent<HTMLTextAreaElement>) => void;
  keyOpportunities: string[];
  additionalOnly: string[];
  showAdditional: boolean;
}

export function useInterviewSession(problem: Problem): UseInterviewSessionResult {
  const starterCode = problem?.starter_code ?? {};
  const languageOptions = useMemo<Language[]>(() => {
    const keys = Object.keys(starterCode).filter(isLanguage) as Language[];
    return keys.length > 0 ? keys : [DEFAULT_LANGUAGE];
  }, [starterCode]);

  const [selectedLanguage, setSelectedLanguage] = useState<Language>(
    languageOptions[0] ?? DEFAULT_LANGUAGE
  );
  const [code, setCode] = useState<string>(starterCode[selectedLanguage] ?? "");
  const [draftMessage, setDraftMessage] = useState("");
  const [activeTab, setActiveTab] = useState<InterviewPanelTab>("chat");

  const transport = useInterviewApi({ problem });
  const {
    rubricRows,
    nitpicks,
    feedbackSummary,
    finalScore,
    didPass,
    keyOpportunities,
    additionalOnly,
    showAdditional,
  } = useFeedbackPanelState(transport.evaluations, transport.completionResult);

  useEffect(() => {
    setSelectedLanguage(languageOptions[0] ?? DEFAULT_LANGUAGE);
  }, [languageOptions]);

  useEffect(() => {
    setCode(starterCode[selectedLanguage] ?? "");
  }, [starterCode, selectedLanguage]);

  useEffect(() => {
    if (
      transport.status === "COMPLETED" &&
      !transport.completionResult &&
      activeTab !== "feedback"
    ) {
      setActiveTab("feedback");
    }
  }, [activeTab, transport.completionResult, transport.status]);

  const handleLanguageChange = useCallback(
    (nextLanguage: Language) => {
      setSelectedLanguage(nextLanguage);
      setCode(starterCode[nextLanguage] ?? "");
    },
    [starterCode]
  );

  const updateCode = useCallback((value: string | undefined) => {
    setCode(value ?? "");
  }, []);

  const handleSend = useCallback(async () => {
    if (!transport.sessionId) {
      return;
    }
    const content = draftMessage.trim();
    if (!content) {
      return;
    }
    setDraftMessage("");
    try {
      await transport.sendChatMessage(content, code);
    } catch {
      setDraftMessage(content);
    }
  }, [code, draftMessage, transport]);

  const handleSubmitCode = useCallback(async () => {
    await transport.submitSolution(code, selectedLanguage);
  }, [code, selectedLanguage, transport]);

  const handleDraftKeyDown = useCallback(
    (event: KeyboardEvent<HTMLTextAreaElement>) => {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        void handleSend();
      }
    },
    [handleSend]
  );

  const hasSession = Boolean(transport.sessionId);

  return {
    languageOptions,
    selectedLanguage,
    code,
    draftMessage,
    messages: transport.messages,
    sessionStatus: transport.status,
    canSubmit: transport.canSubmit,
    activeTab,
    evaluations: transport.evaluations,
    completionResult: transport.completionResult,
    isSending: transport.isSending,
    isSubmittingCode: transport.isSubmittingCode,
    isLoadingFeedback: transport.isLoadingFeedback,
    error: transport.error,
    rubricRows,
    nitpicks,
    feedbackSummary,
    finalScore,
    didPass,
    hasSession,
    setDraftMessage,
    setActiveTab,
    handleLanguageChange,
    updateCode,
    handleSend,
    handleSubmitCode,
    handleDraftKeyDown,
    keyOpportunities,
    additionalOnly,
    showAdditional,
  };
}
