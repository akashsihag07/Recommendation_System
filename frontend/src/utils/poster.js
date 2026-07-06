const BASE_URL = "https://image.tmdb.org/t/p/w342";

export function posterUrl(posterPath) {
  if (!posterPath) return null;
  return `${BASE_URL}${posterPath}`;
}