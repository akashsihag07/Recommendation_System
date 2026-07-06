import { useState } from "react";
import { posterUrl } from "../utils/poster.js";
import { trailerSearchUrl } from "../utils/trailer.js";

function formatVotes(count) {
  if (count >= 1000) return `${(count / 1000).toFixed(1)}k votes`;
  return `${count} votes`;
}

export default function MovieCard({ movie }) {
  const poster = posterUrl(movie.poster);
  const [expanded, setExpanded] = useState(false);

  function handleMove(e) {
    const card = e.currentTarget;
    const rect = card.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    card.style.transform = `perspective(700px) rotateY(${x * 8}deg) rotateX(${-y * 8}deg) translateY(-4px)`;
  }

  function handleLeave(e) {
    e.currentTarget.style.transform = "";
  }

  return (
    <article className="card" onMouseMove={handleMove} onMouseLeave={handleLeave}>
      {poster ? (
        <img className="card-poster" src={poster} alt={movie.title} loading="lazy" />
      ) : (
        <div className="card-poster card-poster-fallback">{movie.title.charAt(0)}</div>
      )}

      <div className="card-body">
        <h3 className="card-title">{movie.title}</h3>
        <p className="card-meta">
          {movie.year || "Year unknown"}
          {movie.runtime ? ` \u00b7 ${movie.runtime} min` : ""}
        </p>

        <p className="card-rating-line">
          {movie.rating.toFixed(1)}{"\u2605"} ({formatVotes(movie.votes)})
        </p>

        <div className="card-genres">
          {movie.genres.slice(0, 3).map((g) => (
            <span key={g} className="chip-sm">{g}</span>
          ))}
        </div>

        <p className={expanded ? "card-overview card-overview-open" : "card-overview"}>
          {movie.desc || "No description available."}
        </p>

        {movie.desc && movie.desc.length > 100 && (
          <button className="more-btn" onClick={() => setExpanded(!expanded)}>
            {expanded ? "less" : "more"}
          </button>
        )}

        <a className="trailer-link" href={trailerSearchUrl(movie.title, movie.year)} target="_blank" rel="noopener noreferrer">
          {"\u25b6"} Watch Trailer
        </a>
      </div>
    </article>
  );
}