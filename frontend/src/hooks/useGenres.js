import { useEffect, useState } from "react";
import { fetchGenres } from "../api/genres.js";

// Loads the list of genres once when the app starts. Keeping this in a hook
// keeps App.jsx focused on layout instead of fetch plumbing.
export function useGenres() {
  const [genres, setGenres] = useState([]);

  useEffect(() => {
    fetchGenres()
      .then(setGenres)
      .catch(() => setGenres([])); // if the backend is down we just show none
  }, []);

  return genres;
}
