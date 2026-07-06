// There iss no direct trailer link in our dataset so i have used simple youtube search link instead 
export function trailerSearchUrl(title, year) {
  const query = encodeURIComponent(`${title} ${year || ""} trailer`);
  return `https://www.youtube.com/results?search_query=${query}`;
}