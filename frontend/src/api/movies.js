// search.js
// Movie search API.

import { getJSON } from "./client.js";

export async function searchTitles(query) {
  try {
    const data = await getJSON(
      `/movies/search?q=${encodeURIComponent(query)}`
    );

    return data.results;
  } catch {
    return [];
  }
}