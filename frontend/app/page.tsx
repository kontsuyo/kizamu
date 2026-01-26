import Link from "next/link";
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
      <article>
        <div>
          <Link href={`/items/${item.id}`}>
            <h2>
              {item.brand} {item.model_name}
            </h2>
            <h3>{item.leather}</h3>
          </Link>
        </div>
        <div>
          <Link href={`/photos/${item.id}`}>
            <img src={item.image} alt="" />
          </Link>
        </div>
        <div>
          <Link href={`/users/${item.user}`}>
            <p>{item.user}</p>
          </Link>
          <time dateTime={item.created_at.slice(0, 10)}>
            {item.created_at.slice(0, 10)}
          </time>
          <p>{item.note}</p>
        </div>
      </article>
    </li>
  ));
  return (
    <div>
      <ul>{listItems}</ul>
    </div>
  );
}
