import { Item } from "./types";

export async function fetchItems(): Promise<Item[]> {
  const url = "http://backend:8000/";
  const res = await fetch(url);
  const data = await res.json();
  return data.results;
}
