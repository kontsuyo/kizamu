"use client";
import { useEffect, useState } from "react";

import Cookies from "js-cookie";
import { getApiUrl } from "@/src/lib/api";

export default function ProfilePage() {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const fetchProfile = async () => {
      // 保存した鍵をポケット(cookie)から取り出す
      const token = Cookies.get("access_token");

      if (!token) {
        console.log("鍵がありません。ログインしてください。");
        return;
      }

      const baseUrl = getApiUrl();

      try {
        // 鍵をヘッダーに入れてリクエストを送る
        const response = await fetch(`${baseUrl}/api/auth/user/`, {
          method: "GET",
          headers: {
            "Content-type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          setUser(data);
        } else {
          console.error(
            "プロフィール取得失敗。トークンが切れている可能性があります。",
          );
        }
      } catch (error) {
        console.error("通信エラー:", error);
      }
    };
    fetchProfile();
  }, []);
  if (!user) {
    return <p>読み込み中、または未ログイン...</p>;
  }
  return (
    <div>
      <h2>ようこそ、{user.username}</h2>
      <p>メールアドレス: {user.email}</p>
    </div>
  );
}
