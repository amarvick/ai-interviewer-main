export interface SubmissionPayload {
  problem_id: string;
  code_submitted: string;
  language: string;
}

export interface SubmissionResponse {
  id: string;
  user_id: string;
  problem_id: string;
  code_submitted: string;
  language: string;
  result: "pass" | "fail";
  tests_passed: number;
  tests_total: number;
  error?: string | null;
  created_at?: string;
}
