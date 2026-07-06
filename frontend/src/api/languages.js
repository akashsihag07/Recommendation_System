import { getJSON } from "./client.js";

// Gets the languages available in the dropdown.
export async function fetchLanguages() {
  const data = await getJSON("/languages");
  return data.languages;
}
