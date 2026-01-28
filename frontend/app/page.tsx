import Link from "next/link";
import { Post, PaginatedResponse } from "./types";

async function fetchPosts(): Promise<Post[]> {
  const url = "http://backend:8000/";
  try {
    const response = await fetch(url);
    if (!response.ok) {
      return [];
    }
    const json: PaginatedResponse<Post> = await response.json();
    return json.results;
  } catch (error) {
    console.error("データ取得エラー:", error);
    return [];
  }
}

export default async function Home() {
  const posts = await fetchPosts();
  const listPost = posts.map((post: Post) => (
    <li key={post.id}>
      <article>
        <div>
          <Link href={`/items/${post.item_id}`}>
            <h2>
              {post.brand} {post.model_name}
            </h2>
            <h3>{post.leather}</h3>
          </Link>
        </div>
        <div>
          <Link href={`/photos/${post.id}`}>
            <img src={post.image} alt="" />
          </Link>
        </div>
        <div>
          <Link href={`/users/${post.user}`}>
            <p>{post.user}</p>
          </Link>
          <time dateTime={post.created_at.slice(0, 10)}>
            {post.created_at.slice(0, 10)}
          </time>
          <p>{post.note}</p>
        </div>
      </article>
    </li>
  ));
  return (
    <div>
      <ul>{listPost}</ul>
    </div>
  );
}
