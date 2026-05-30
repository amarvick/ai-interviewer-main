import type { TestCase } from "./testcase";
import type { Language } from "./language";

export type Difficulty = "easy" | "medium" | "hard" | string;

export interface Problem {
  id: string;
  slug: string;
  title: string;
  description: string;
  difficulty: Difficulty;
  category: string;
  starter_code: Partial<Record<Language, string>>;
  is_passed?: boolean;
  test_cases: TestCase[];
}

export interface ProblemList {
  id: string;
  name: string;
  icon_url: string;
}

export interface ProblemListProblemsResponse {
  name: string;
  problems: Problem[];
}

export interface ProblemSearchPageParams {
  problemListId: string;
  search?: string;
  page?: number;
  pageSize?: number;
}

export interface ProblemSearchPageResponse {
  name: string;
  problems: Problem[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
  has_next_page: boolean;
  has_previous_page: boolean;
}
