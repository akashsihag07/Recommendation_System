import { useEffect, useState } from "react";
import { searchTitles } from "../api/movies.js";

// Optional favorite movie field.
// Handles title suggestions as the user types and keeps track of the
// selected movie. The parent only needs the final value through onChange.
export default function FavoriteSearch({ value, onChange }) {
  const [suggestions, setSuggestions] = useState([]);

  // Small delay so we don't hit the API on every keystroke.
  useEffect(() => {
    if (value.trim().length < 2) {
      setSuggestions([]);
      return;
    }
    const timer = setTimeout(async () => {
      setSuggestions(await searchTitles(value));
    }, 300);
    return () => clearTimeout(timer);
  }, [value]);

  function pick(title) {
    onChange(title);
    setSuggestions([]);
  }

  return (
    <div className="form-block fav-block">
      <label className="form-label">
        Loved a movie? Get more like it (optional)
      </label>
      <input
        type="text"
        className="fav-input"
        placeholder="e.g. Inception"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
      {suggestions.length > 0 && (
        <ul className="suggestions">
          {suggestions.map((s) => (
            <li key={s} onClick={() => pick(s)}>
              {s}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
