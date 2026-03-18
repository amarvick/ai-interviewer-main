export const LANGUAGES = ["python", "javascript", "java", "cpp"] as const;

export type Language = (typeof LANGUAGES)[number];

export const DEFAULT_LANGUAGE: Language = "javascript";

export function isLanguage(value: string): value is Language {
  return (LANGUAGES as readonly string[]).includes(value);
}
