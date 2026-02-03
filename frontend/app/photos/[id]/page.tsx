import type { Photo, PhotoPageProps } from "@/app/types";
import Link from "next/link";

async function fetchPhotoInfo(photoId: number): Promise<Photo | null> {
  const url = `${process.env.NEXT_PUBLIC_API_URL}photos/${photoId}/`;
  // const url = `http://backend:8000/photos/${photoId}/`;
  try {
    const response = await fetch(url);
    if (!response.ok) {
      return null;
    }
    const json: Photo = await response.json();
    console.log(json);
    return json;
  } catch (error) {
    console.error("データ取得エラー:", error);
    return null;
  }
}

export default async function PhotoPage({ params }: PhotoPageProps) {
  const resolveParams = await params;
  const photoId = parseInt(resolveParams.id, 10);
  const photo = await fetchPhotoInfo(photoId);

  if (!photo) {
    return <div>写真が見つかりません</div>;
  }

  return (
    <>
      <div>
        <img src={photo.image} alt="アイテムの画像" />
      </div>
      <div>
        <h2>
          {photo.item.brand} {photo.item.model_name}
        </h2>
        <h3>{photo.item.leather}</h3>
      </div>
      <Link href={`/items/${photo.item.id}`}>
        <button type="button">View album</button>
      </Link>
      <div>
        <p>
          <Link href={`/users/${photo.user}`}>{photo.user}</Link>{" "}
          {photo.wore_on}
        </p>
        <p>{photo.note}</p>
      </div>
    </>
  );
}
