"use client";
import React, { useState } from "react";

import Cookies from "js-cookie";

import { getApiUrl } from "@/src/lib/api";
import { useRouter } from "next/router";

export default function ItemCreatePage() {
  const [brand, setBrand] = useState<string>("");
  const [modelName, setModelName] = useState<string>("");

  async function handleItemCreate(e: React.FormEvent) {
    e.preventDefault();

    const baseUrl = getApiUrl();
    const url = `${baseUrl}/items/create/`;
    const token = Cookies.get("access_token");
    const formData = {
      brand: brand,
      model_name: modelName,
    };
    // 英数字・スペース・ハイフンのみ許可する正規表現
    const alphaNumeric = /^[a-zA-Z0-9\s-]+$/;

    if (!alphaNumeric.test(brand) || !alphaNumeric.test(modelName)) {
      alert("ブランド名とモデル名は英数字で入力してください");
      return;
    }

    try {
      const res = await fetch(url, {
        method: "POST",
        headers: {
          "Content-type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        const errorData = await res.json();
        console.error(errorData);
        return;
      }

      const data = await res.json();
      alert("ブーツを登録しました！");
      window.location.href = `/users/${data.user}`;
    } catch (error) {
      console.error("通信エラー：", error);
    }
  }
  return (
    <div>
      <h2>ブーツ登録</h2>
      <p>
        検索性を高めるため、ブランド名とモデル名はアルファベット（例: Red
        Wing）での入力をお願いしています。
      </p>
      <div>
        <form onSubmit={handleItemCreate}>
          <input
            type="text"
            value={brand}
            onChange={(e) => setBrand(e.target.value)}
            placeholder="ブランド"
            pattern="^[a-zA-Z0-9\s-]+$"
            title="英数字、スペース、ハイフンのみ使用できます" // エラー時に出る説明
            required
          />
          <input
            type="text"
            value={modelName}
            onChange={(e) => setModelName(e.target.value)}
            placeholder="モデル"
            pattern="^[a-zA-Z0-9\s-]+$"
            title="英数字、スペース、ハイフンのみ使用できます" // エラー時に出る説明
            required
          />
          <button type="submit">登録する</button>
        </form>
      </div>
    </div>
  );
}
