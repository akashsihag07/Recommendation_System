// Maps the short language codes from the data (e.g. "hi") to readable names for
// the dropdown. Anything not listed just shows its raw code as a fallback.
const NAMES = {
  en: "English", hi: "Hindi", ta: "Tamil", te: "Telugu", ml: "Malayalam",
  kn: "Kannada", bn: "Bengali", mr: "Marathi", pa: "Punjabi", ur: "Urdu",
  fr: "French", es: "Spanish", it: "Italian", de: "German", ja: "Japanese",
  ko: "Korean", zh: "Chinese", cn: "Chinese", ru: "Russian", pt: "Portuguese",
  tr: "Turkish", ar: "Arabic", th: "Thai", fa: "Persian", sv: "Swedish",
  da: "Danish", nl: "Dutch", pl: "Polish", id: "Indonesian",
};

export function languageName(code) {
  return NAMES[code] || code.toUpperCase();
}
