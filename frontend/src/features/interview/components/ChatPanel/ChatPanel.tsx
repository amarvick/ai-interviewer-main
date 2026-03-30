import { useEffect, useRef } from "react";
import type { KeyboardEvent } from "react";
import type { ChatMessage } from "@/features/interview/utils/interview";

interface ChatPanelProps {
  messages: ChatMessage[];
  draftMessage: string;
  onDraftChange: (value: string) => void;
  onKeyDown: (event: KeyboardEvent<HTMLTextAreaElement>) => void;
  onSend: () => void;
  isSending: boolean;
  isSubmittingCode: boolean;
  hasSession: boolean;
}

export default function ChatPanel({
  messages,
  draftMessage,
  onDraftChange,
  onKeyDown,
  onSend,
  isSending,
  isSubmittingCode,
  hasSession,
}: ChatPanelProps) {
  const chatRef = useRef<HTMLDivElement | null>(null);
  const inputRef = useRef<HTMLTextAreaElement | null>(null);

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
    const lastMessage = messages[messages.length - 1];
    if (lastMessage?.role === "ai") {
      inputRef.current?.focus();
    }
  }, [messages]);

  const disableSend =
    isSending || isSubmittingCode || !hasSession || !draftMessage.trim();

  return (
    <>
      <div className="interview-chat-messages" ref={chatRef}>
        {messages.length === 0 && (
          <p className="interview-chat-empty">
            Interview messages will appear here when the session starts.
          </p>
        )}
        {messages.map((message) => (
          <article
            key={message.id}
            className={`chat-bubble ${message.role === "ai" ? "ai" : "you"}`}
          >
            <p className="chat-bubble-role">
              {message.role === "ai" ? "Interviewer" : "You"}
            </p>
            <p className="chat-bubble-text">{message.content}</p>
          </article>
        ))}
      </div>
      <footer className="interview-chat-input-wrap">
        <textarea
          ref={inputRef}
          value={draftMessage}
          onChange={(event) => onDraftChange(event.target.value)}
          onKeyDown={onKeyDown}
          placeholder="Explain your thinking, ask a clarification, or answer a follow-up..."
          rows={3}
        />
        <button type="button" onClick={onSend} disabled={disableSend}>
          {isSending ? "Sending..." : "Send"}
        </button>
      </footer>
    </>
  );
}
