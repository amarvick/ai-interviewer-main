import type { Problem } from "@/types/problem";
import {
  ProblemPageCodeEditor,
  ProblemPageEditorToolbar,
} from "@/features/problem";
import SplitPane from "@/components/SplitPane/SplitPane";
import { useInterviewSession } from "@/features/interview/hooks/useInterviewSession";
import ChatPanel from "@/features/interview/components/ChatPanel/ChatPanel";
import FeedbackPanel from "@/features/interview/components/FeedbackPanel/FeedbackPanel";
import HistoryPanel from "@/features/interview/components/HistoryPanel/HistoryPanel";
import "./InterviewPageEditor.css";

interface InterviewPageEditorProps {
  problem: Problem;
}

export default function InterviewPageEditor({
  problem,
}: InterviewPageEditorProps) {
  const {
    languageOptions,
    selectedLanguage,
    code,
    draftMessage,
    messages,
    sessionStatus,
    canSubmit,
    activeTab,
    isSending,
    isSubmittingCode,
    isLoadingFeedback,
    error,
    rubricRows,
    feedbackSummary,
    finalScore,
    didPass,
    hasSession,
    evaluations,
    setDraftMessage,
    setActiveTab,
    handleLanguageChange,
    updateCode,
    handleSend,
    handleSubmitCode,
    handleDraftKeyDown,
    completionResult,
    keyOpportunities,
    additionalOnly,
    showAdditional,
  } = useInterviewSession(problem);

  return (
    <div className="interview-editor-shell">
      <SplitPane
        orientation="vertical"
        defaultPrimarySize={66}
        minPrimarySize={46}
        maxPrimarySize={84}
        className="interview-inner-split"
        primary={
          <section
            className="editor-panel editor-panel-active"
            aria-label="Code editor"
          >
            <ProblemPageEditorToolbar
              selectedLanguage={selectedLanguage}
              handleLanguageChange={handleLanguageChange}
              languageOptions={languageOptions}
              onSubmit={handleSubmitCode}
              isSubmitting={isSubmittingCode}
              isSubmitDisabled={!canSubmit}
              submitLabel="Submit Code"
              submittingLabel="Submitting..."
            />
            <ProblemPageCodeEditor
              selectedLanguage={selectedLanguage}
              updateCode={updateCode}
              code={code}
              readOnly={false}
              className="editor-shell-active"
            />
          </section>
        }
        secondary={
          <section
            className="interview-chat-panel"
            aria-label="AI interview panel"
          >
            <header className="interview-chat-header">
              <span>AI Interview Panel</span>
            </header>
            <div
              className="interview-panel-tabs"
              role="tablist"
              aria-label="Interview tabs"
            >
              <button
                type="button"
                role="tab"
                aria-selected={activeTab === "chat"}
                className={`interview-tab ${
                  activeTab === "chat" ? "active" : ""
                }`}
                onClick={() => setActiveTab("chat")}
              >
                Chat
              </button>
              <button
                type="button"
                role="tab"
                aria-selected={activeTab === "feedback"}
                className={`interview-tab ${
                  activeTab === "feedback" ? "active" : ""
                }`}
                onClick={() => {
                  if (sessionStatus === "COMPLETED") {
                    setActiveTab("feedback");
                  }
                }}
                disabled={sessionStatus !== "COMPLETED"}
              >
                Feedback
              </button>
              <button
                type="button"
                role="tab"
                aria-selected={activeTab === "history"}
                className={`interview-tab ${
                  activeTab === "history" ? "active" : ""
                }`}
                onClick={() => setActiveTab("history")}
              >
                History
              </button>
            </div>
            {activeTab === "chat" && (
              <ChatPanel
                messages={messages}
                draftMessage={draftMessage}
                onDraftChange={setDraftMessage}
                onKeyDown={handleDraftKeyDown}
                onSend={handleSend}
                isSending={isSending}
                isSubmittingCode={isSubmittingCode}
                hasSession={hasSession}
              />
            )}
            {activeTab === "feedback" && (
              <div className="interview-feedback-panel">
                <FeedbackPanel
                  completionResult={completionResult}
                  isLoading={isLoadingFeedback}
                  rubricRows={rubricRows}
                  feedbackSummary={feedbackSummary}
                  finalScore={finalScore}
                  didPass={didPass}
                  keyOpportunities={keyOpportunities}
                  additionalOnly={additionalOnly}
                  showAdditional={showAdditional}
                />
              </div>
            )}
            {activeTab === "history" && (
              <div className="interview-history-panel">
                <HistoryPanel evaluations={evaluations} />
              </div>
            )}
            {error && <p className="interview-chat-error">{error}</p>}
          </section>
        }
      />
    </div>
  );
}
