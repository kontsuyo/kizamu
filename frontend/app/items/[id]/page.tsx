import Link from "next/link";
import { Item, ItemPageProps, Photo } from "../../types";

async function fetchItem(itemId: number): Promise<Item | null> {
  const url = `${process.env.NEXT_PUBLIC_API_URL}items/${itemId}/`;
  try {
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) {
      return null;
    }
    const json: Item = await response.json();
    return json;
  } catch (error) {
    console.error("データ取得エラー:", error);
    return null;
  }
}

export default async function ItemPage({ params }: ItemPageProps) {
  const resolvedParams = await params;
  const itemId = parseInt(resolvedParams.id, 10);
  const item = await fetchItem(itemId);
  if (!item) {
    return (
      <div>
        <p>アイテムが見つかりません</p>
      </div>
    );
  }
  const listPhotos = item.photos.map((photo: Photo) => (
    <li key={item.id}>
      <Link href={`/photos/${photo.id}`}>
        <img src={photo.image} alt="アイテム画像" />
      </Link>
    </li>
  ));
  return (
    <div>
      <div>
        <h2>
          {item.brand} {item.model_name}
        </h2>
        <h3>{item.leather}</h3>
      </div>
      <div>
        <ul>{listPhotos}</ul>
      </div>
    </div>
  );
}
