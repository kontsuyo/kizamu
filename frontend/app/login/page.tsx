"use client";
import Cookies from "js-cookie";
import { getApiUrl } from "@/src/lib/api";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const router = useRouter();

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();

    const baseUrl = getApiUrl();
    try {
      const res = await fetch(`${baseUrl}/api/auth/login`, {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await res.json();

      if (res.ok) {
        Cookies.set("access_token", data.access, { expires: 1 });
        Cookies.set("refresh_token", data.refresh, { expires: 7 });

        console.log("ログイン成功");
        router.push(`/items/${username}`);
      } else {
        alert("ログインに失敗しました。ユーザー名かパスワードが違います。");
      }
    } catch (error) {
      console.error("通信エラー：", error);
    }
  }

  return (
    <div>
      <h2>ログインページ</h2>
      <form onSubmit={handleLogin} method="post">
        <input
          type="text"
          placeholder="ユーザー名"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="パスワード"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">ログイン</button>
      </form>
    </div>
  );
}
