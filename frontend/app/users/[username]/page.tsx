"use client";
import { useEffect, useState } from "react";
import Link from "next/link";

import Cookies from "js-cookie";

import type { ProfilePageProps, UserProfile } from "@/app/types";
import { getApiUrl } from "@/src/lib/api";
import React from "react";

export default function ProfilePage({
  params,
}: {
  params: Promise<{ username: string }>;
}) {
  const baseUrl = getApiUrl();
  const { username } = React.use(params);
  const [profileUser, setProfileUser] = useState<any>(null);
  const [me, setMe] = useState<any>(null);

  useEffect(() => {
    // このページの持ち主の情報を取得（誰でも閲覧可能)
    fetch(`${baseUrl}/users/${username}/`)
      .then((res) => res.json())
      .then((data) => setProfileUser(data));

    // ログインユーザーの情報を取得（ログインしていれば）
    const token = Cookies.get("access_token");
    console.log("取得したトークン：", token);
    if (token) {
      fetch(`${baseUrl}/api/auth/user/`, {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((res) => (res.ok ? res.json() : null))
        .then((data) => setMe(data));
    }
  }, [username, baseUrl]);

  // meとprofileUserを確認するのはTypeErrorでアプリがクラッシュするのを防ぐため
  const isMypage = me && profileUser && me.username === profileUser[0].username;

  return (
    <div>
      <h2>{username}</h2>
      {isMypage && (
        <div>
          <button onClick={() => (window.location.href = "/items/create")}>
            + ブーツを登録する
          </button>
        </div>
      )}
    </div>
  );
}

// async function fetchUserItems(username: string): Promise<UserProfile | null> {
//   const url = `${process.env.NEXT_PUBLIC_API_URL}/users/${username}/`;
//   try {
//     const response = await fetch(url, { cache: "no-store" });
//     if (!response.ok) {
//       return null;
//     }
//     const json = await response.json();
//     return json[0];
//   } catch (error) {
//     console.error("データ取得エラー: ", error);
//     return null;
//   }
// }

// export default async function ProfilePage({ params }: ProfilePageProps) {
//   const resolveParams = await params;
//   const username = resolveParams.username;
//   const userItems = await fetchUserItems(username);
//   if (!userItems) {
//     return (
//       <div>
//         <h2>{username}</h2>
//         <p></p>
//       </div>
//     );
//   }
//   const photos = userItems.items
//     .filter((item) => item.photos.length > 0)
//     .map((item) => ({
//       itemId: item.id,
//       image: item.photos[0].image,
//     }));

//   const photoList = photos.map((photo, index) => (
//     <li key={index}>
//       <Link href={`/items/${photo.itemId}`}>
//         <img src={photo.image} alt="アイテム画像" />
//       </Link>
//     </li>
//   ));
//   return (
//     <div>
//       <div>
//         <h2>{username}</h2>
//       </div>
//       <div>
//         <ul>{photoList}</ul>
//       </div>
//     </div>
//   );
// }
