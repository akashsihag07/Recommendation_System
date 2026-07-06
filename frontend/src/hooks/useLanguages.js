import { useEffect, useState } from "react";
import { fetchLanguages } from "../api/languages.js";

// Loads the available languages once when the app starts.
export function useLanguages() {
  const [languages, setLanguages] = useState([]);

  useEffect(() => {
    fetchLanguages()
      .then(setLanguages)
      .catch(() => setLanguages([]));
  }, []);

  return languages;
}
