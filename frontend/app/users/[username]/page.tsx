import type { Item, Photo, ProfilePageProps, UserProfile } from "@/app/types";

async function fetchUser(username: string): Promise<UserProfile[] | null> {
  const url = `http://backend:8000/users/${username}/`;
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`レスポンスステータス: ${response.status}`);
    }
    const json: UserProfile[] = await response.json();
    return json;
  } catch (error) {
    console.error("データ取得エラー:", error);
    return null;
  }
}

async function getImageUrl(username: string): Promise<string[]> {
  const users = await fetchUser(username);
  if (!users || users.length === 0) {
    return [];
  }
  const user = users[0];
  const imageUrls = user.items
    .filter((item) => item.photos && item.photos.length > 0)
    .map((item) => item.photos[0].image);
  return imageUrls;
}

export default async function ProfilePage({ params }: ProfilePageProps) {
  const resolvedParams = await params;
  const username = resolvedParams.username;
  const urls = await getImageUrl(username);
  const listImage = urls.map((url, index) => (
    <li key={index}>
      <img src={url} alt="アイテムの画像" />
    </li>
  ));
  return (
    <div>
      <div>
        <h2>{username}</h2>
      </div>
      <div>
        <ul>{listImage}</ul>
      </div>
    </div>
  );
}
