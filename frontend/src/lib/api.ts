export const getApiUrl = () => {
  // ブラウザ（Client Side）で実行されている場合
  if (typeof window !== "undefined") {
    return process.env.NEXT_PUBLIC_API_URL;
  }
  // サーバーサイド（SSR/App RouterのServer Component）で実行されている場合
  // サーバーサイド用変数がなければ、フロント用をフォールバックにする
  return process.env.INTERNAL_API_URL || process.env.NEXT_PUBLIC_API_URL;
};
