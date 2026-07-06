import { postJSON } from "./client.js";

// Sends the user's preferences to the backend and gets the ranked movies back.
export async function fetchRecommendations(prefs) {
  return postJSON("/recommend", prefs);
}
