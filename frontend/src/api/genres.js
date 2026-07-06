import { getJSON } from "./client.js";

// Gets the full list of genres for the form chips.
export async function fetchGenres() {
  const data = await getJSON("/genres");
  return data.genres;
}
