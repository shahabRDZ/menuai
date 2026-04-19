export type Language = {
  code: string;
  label: string;
};

export const LANGUAGES: Language[] = [
  { code: "en", label: "English" },
  { code: "fa", label: "Persian" },
  { code: "ar", label: "Arabic" },
  { code: "tr", label: "Turkish" },
  { code: "de", label: "German" },
  { code: "fr", label: "French" },
  { code: "es", label: "Spanish" },
  { code: "ru", label: "Russian" },
];

export function languageLabel(code: string): string {
  return LANGUAGES.find((l) => l.code === code)?.label ?? code.toUpperCase();
}
