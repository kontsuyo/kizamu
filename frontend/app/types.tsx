export interface Item {
  id: number;
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
