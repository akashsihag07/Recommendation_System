import Header from "./components/Header.jsx";
import PreferenceForm from "./components/PreferenceForm.jsx";
import ResultsGrid from "./components/ResultsGrid.jsx";

import { useGenres } from "./hooks/useGenres.js";
import { useLanguages } from "./hooks/useLanguages.js";
import { useRecommendations } from "./hooks/useRecommendations.js";

export default function App() {
  const genres = useGenres();
  const languages = useLanguages();
  const { movies, loading, searched, error, run } = useRecommendations();

  return (
    <div className="page">
      <Header />
      <main className="content">
        <PreferenceForm
          genres={genres}
          languages={languages}
          onSubmit={run}
          loading={loading}
        />
        <ResultsGrid
          movies={movies}
          loading={loading}
          searched={searched}
          error={error}
        />
      </main>
      <footer className="footer">
        <p>WatchHub {"\u2014"} find your next movie.</p>
        <p>
          Movie data from{" "}
          <a href="https://www.themoviedb.org/" target="_blank" rel="noopener noreferrer">
            TMDB
          </a>
        </p>
      </footer>
    </div>
  );
}
