import type {
  InterviewCompletionResponse,
  InterviewSessionDetailResponse,
  InterviewSessionStatus,
} from "@/types/interview";
import type { ChatMessage } from "@/features/interview/utils/interview";
import { sortMessagesByTime } from "@/features/interview/utils/interview";

export interface NormalizedSessionDetail {
  id: string;
  status: InterviewSessionStatus;
  canSubmit: boolean;
  evaluations: InterviewSessionDetailResponse["evaluations"];
  messages: ChatMessage[];
}

export const adaptSessionDetail = (
  detail: InterviewSessionDetailResponse
): NormalizedSessionDetail => {
  const messages = sortMessagesByTime(
    detail.messages
      .filter(
        (message) => message.role === "assistant" || message.role === "user"
      )
      .map<ChatMessage>((message) => ({
        id: message.id,
        role: message.role === "assistant" ? "ai" : "you",
        content: message.content,
        createdAt: new Date(message.created_at).getTime(),
      }))
  );

  return {
    id: detail.id,
    status: detail.status,
    canSubmit: Boolean(detail.can_code),
    evaluations: detail.evaluations ?? [],
    messages,
  };
};

export const adaptCompletionResponse = (
  completion: InterviewCompletionResponse
): InterviewCompletionResponse => ({
  ...completion,
  strengths: completion.strengths ?? [],
  gaps: completion.gaps ?? [],
  next_steps: completion.next_steps ?? [],
});
