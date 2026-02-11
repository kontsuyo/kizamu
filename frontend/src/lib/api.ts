export const getApiUrl = () => {
  if (typeof window !== "undefined") {
    // ブラウザからリクエストを飛ばす場合（localhost:8000）
    return process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  }
  // サーバーサイド（Dockerコンテナ間など）から飛ばす場合（backend:8000）
  return process.env.INTERNAL_API_URL || "http://backend:8000";
};
