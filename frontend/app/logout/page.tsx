"use client";
import Cookies from "js-cookie";

export default function LogoutButton() {
  function handleLogout() {
    Cookies.remove("access_token");
    Cookies.remove("refresh_token");

    console.log("ログアウトしました");

    window.location.href = "/login";
  }

  return <button onClick={handleLogout}>ログアウト</button>;
}
