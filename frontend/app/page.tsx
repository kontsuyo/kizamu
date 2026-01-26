import { Item, PaginatedResponse } from "./types";

async function fetchItems(): Promise<Item[]> {
  const url = "http://backend:8000/";
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`レスポンスステータス: ${response.status}`);
    }
    const json: PaginatedResponse<Item> = await response.json();
    return json.results;
  } catch (error) {
    console.error("データ取得エラー:", error);
    return [];
  }
}

export default async function Home() {
  const results = await fetchItems();
  const listItems = results.map((item: Item) => (
    <li key={item.id}>
      <div>
        {item.brand} {item.model_name}
      </div>
      <div>{item.leather}</div>
      <div>
        <img src={item.image} alt="" />
      </div>
      <div>
        {item.user} {item.created_at}
      </div>
    </li>
  ));
  return (
    <div>
      <ul>{listItems}</ul>
    </div>
  );
}
