import { type Language, isLanguage } from "@/types/language";
interface ProblemPageEditorToolbarProps {
  selectedLanguage: Language;
  handleLanguageChange: (nextLanguage: Language) => void;
  languageOptions: Language[];
  onSubmit: () => void;
  isSubmitting: boolean;
  isSubmitDisabled?: boolean;
  submitLabel?: string;
  submittingLabel?: string;
}

const LANGUAGE_LABELS: Record<Language, string> = {
  python: "Python",
  javascript: "JavaScript",
  java: "Java",
  cpp: "C++",
};

export default function ProblemPageEditorToolbar({
  selectedLanguage,
  handleLanguageChange,
  languageOptions,
  onSubmit,
  isSubmitting,
  isSubmitDisabled = false,
  submitLabel = "Submit",
  submittingLabel = "Submitting...",
}: ProblemPageEditorToolbarProps) {
  return (
    <div className="editor-toolbar">
      <label htmlFor="editor-language">Language</label>
      <select
        id="editor-language"
        value={selectedLanguage}
        onChange={(event) => {
          const value = event.target.value;
          if (isLanguage(value)) {
            handleLanguageChange(value);
          }
        }}
      >
        {languageOptions.map((language) => (
          <option key={language} value={language}>
            {LANGUAGE_LABELS[language] ?? language}
          </option>
        ))}
      </select>

      <div className="toolbar-actions">
        <button
          type="button"
          onClick={onSubmit}
          disabled={isSubmitting || isSubmitDisabled}
        >
          {isSubmitting ? submittingLabel : submitLabel}
        </button>
      </div>
    </div>
  );
}
