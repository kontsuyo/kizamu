"use client";
import { useState } from "react";

import { getApiUrl } from "@/src/lib/api";

interface Form {
  username: string;
  email: string;
  password1: string;
  password2: string;
}

export default function RegisterPage() {
  const [formData, setFormData] = useState<Form>({
    username: "",
    email: "",
    password1: "",
    password2: "",
  });

  function handleUserNameChange(e: React.ChangeEvent<HTMLInputElement>) {
    setFormData({
      ...formData,
      username: e.target.value,
    });
  }

  function handleEmailChange(e: React.ChangeEvent<HTMLInputElement>) {
    setFormData({
      ...formData,
      email: e.target.value,
    });
  }

  function handlePasswordChange(e: React.ChangeEvent<HTMLInputElement>) {
    setFormData({
      ...formData,
      password1: e.target.value,
    });
  }

  function handleConfirmPasswordChange(e: React.ChangeEvent<HTMLInputElement>) {
    setFormData({
      ...formData,
      password2: e.target.value,
    });
  }

  async function handleRegister(e: React.FormEvent) {
    e.preventDefault();
    const baseUrl = getApiUrl();
    const url = `${baseUrl}/api/auth/registration/`;
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });
      if (!response.ok) {
        return null;
      }
      const result = await response.json();
      console.log(result);
      return result;
    } catch (error) {
      console.error("ユーザー登録エラー：", error);
      return null;
    }
  }

  return (
    <div>
      <h1>Register Page</h1>
      <form onSubmit={handleRegister} method="post">
        <div>
          <label htmlFor="username">ユーザー名</label>
          <input
            type="text"
            name="username"
            id="username"
            value={formData.username}
            onChange={handleUserNameChange}
            required
          />
        </div>
        <div>
          <label htmlFor="email">メールアドレス</label>
          <input
            type="text"
            name="email"
            id="email"
            value={formData.email}
            onChange={handleEmailChange}
            required
          />
        </div>
        <div>
          <label htmlFor="password1">パスワード</label>
          <input
            type="password"
            name="password1"
            id="password1"
            value={formData.password1}
            onChange={handlePasswordChange}
            required
          />
        </div>
        <div>
          <label htmlFor="password2">パスワードの確認</label>
          <input
            type="password"
            name="password2"
            id="password2"
            value={formData.password2}
            onChange={handleConfirmPasswordChange}
            required
          />
        </div>
        <p>
          {formData.username} {formData.email} {formData.password1}{" "}
          {formData.password2}
        </p>
        <div>
          <button type="submit">登録する</button>
        </div>
      </form>
    </div>
  );
}
