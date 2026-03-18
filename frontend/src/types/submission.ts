import type { Language } from "./language";

export interface SubmissionPayload {
  problem_id: string;
  code_submitted: string;
  language: Language;
}

export interface SubmissionResponse {
  id: string;
  user_id: string;
  problem_id: string;
  code_submitted: string;
  language: Language;
  result: "pass" | "fail";
  tests_passed: number;
  tests_total: number;
  error?: string | null;
  created_at?: string;
}
