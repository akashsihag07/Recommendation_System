import { useState } from "react";
import { fetchRecommendations } from "../api/recommend.js";

// Holds everything about a recommendation search: the results, whether a request
// is in flight, whether the user has searched yet, and any error message.
// Components just call run(prefs) and read the state back.
export function useRecommendations() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [error, setError] = useState("");

  async function run(prefs) {
    setLoading(true);
    setError("");
    try {
      const results = await fetchRecommendations(prefs);
      setMovies(results);
    } catch (e) {
      setMovies([]);
      setError("Couldn't reach the recommender. Is the backend running?");
    } finally {
      setLoading(false);
      setSearched(true);
    }
  }

  return { movies, loading, searched, error, run };
}
