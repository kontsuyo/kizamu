export interface Post {
  id: number;
  item_id: number;
  brand: string;
  model_name: string;
  leather: string;
  image: string;
  note: string;
  user: string;
  created_at: string;
}

export interface PaginatedResponse<T> {
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface Item {
  id: number;
  brand: string;
  model_name: string;
  leather: string;
  user: string;
  created_at: string;
  photos: [];
}

export interface ItemPageProps {
  params: {
    id: string;
  };
}

export interface Photo {
  id: number;
  item: number;
  image: string;
  wore_on: string;
  note: string;
  shared_feed: boolean;
  user: string;
}

export interface UserProfile {
  id: number;
  username: string;
  items: [Item];
}

export interface ProfilePageProps {
  params: {
    username: string;
  };
}
