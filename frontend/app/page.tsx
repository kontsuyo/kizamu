import { fetchItems } from "./fetch-items";
import {Item} from "./types"

export default async function Feed() {
  const results = await fetchItems();
  const listItems = results.map((item: Item) =>
    <li key={item.id}>
      <div>{item.brand} {item.model_name}</div>
      <div>{item.leather}</div>
      <div><img src={item.image} alt="" /></div>
      <div>{item.user} {item.created_at}</div>
    </li>
  )
  return (
    <div>
      <ul>{listItems}</ul>
    </div>
  );
}
