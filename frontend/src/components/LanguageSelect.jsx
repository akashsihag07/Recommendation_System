import { languageName } from "../utils/languageNames.js";

// Language filter.
// The options come from the backend, but we only show languages
// with enough movies to keep the list manageable.
export default function LanguageSelect({ languages, value, onChange }) {
  const worthShowing = languages.filter((l) => l.count >= 20);

  return (
    <div className="form-block">
      <label className="form-label">Language</label>
      <select
        className="lang-select"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        <option value="any">Any language</option>
        {worthShowing.map((l) => (
          <option key={l.code} value={l.code}>
            {languageName(l.code)} 
          </option>
        ))}
      </select>
    </div>
  );
}
