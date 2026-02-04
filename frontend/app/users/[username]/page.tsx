import type { ProfilePageProps, UserProfile } from "@/app/types";
import Link from "next/link";

async function fetchUserItems(username: string): Promise<UserProfile | null> {
  const url = `${process.env.NEXT_PUBLIC_API_URL}/users/${username}/`;
  try {
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) {
      return null;
    }
    const json = await response.json();
    return json[0];
  } catch (error) {
    console.error("データ取得エラー: ", error);
    return null;
  }
}

export default async function ProfilePage({ params }: ProfilePageProps) {
  const resolveParams = await params;
  const username = resolveParams.username;
  const userItems = await fetchUserItems(username);
  if (!userItems) {
    return (
      <div>
        <p>ユーザーが見つかりません</p>
      </div>
    );
  }
  const photos = userItems.items
    .filter((item) => item.photos.length > 0)
    .map((item) => ({
      itemId: item.id,
      image: item.photos[0].image,
    }));

  const photoList = photos.map((photo, index) => (
    <li key={index}>
      <Link href={`/items/${photo.itemId}`}>
        <img src={photo.image} alt="アイテム画像" />
      </Link>
    </li>
  ));
  return (
    <div>
      <div>
        <h2>{userItems.username}</h2>
      </div>
      <div>
        <ul>{photoList}</ul>
      </div>
    </div>
  );
}
