export type Product = {
  id: string;
  name: string;
  description: string;
  price: number;
  category: string;
  image_url: string;
};
export type TryOn = {
  imageBase64: string;
  width: number;
  height: number;
  prompt: string;
  cached: boolean;
};

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, init);
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || "Ocurrió un error inesperado.");
  }
  return response.json() as Promise<T>;
}
export const getProducts = () => request<Product[]>("/api/products");
export const createTryOn = (id: string) =>
  request<TryOn>(`/api/products/${id}/try-on`, { method: "POST" });
