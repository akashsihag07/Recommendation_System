import MovieCard from "./MovieCard.jsx";
import StatusMessage from "./StatusMessage.jsx";

// it Decides what to show below the form
export default function ResultsGrid({ movies, loading, searched, error }) {
  if (loading) return <StatusMessage text={"Finding your matches\u2026"} />;
  if (error) return <StatusMessage text={error} />;

  // only show the empty message once the user has actually run a search
  if (searched && movies.length === 0) {
    return (
      <StatusMessage text="No movies matched those preferences. Try removing a filter or lowering the minimum rating." />
    );
  }

  if (movies.length === 0) return null;

  return (
    <div className="grid">
      {movies.map((m, i) => (
        // title isn't guaranteed unique across the catalogue, so pair it with the
        // index for a stable key
        <MovieCard key={`${m.title}-${i}`} movie={m} />
      ))}
    </div>
  );
}
