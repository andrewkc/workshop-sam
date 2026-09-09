import { useEffect, useState } from "react";
import { Product, getProducts } from "./api";
import Catalog from "./components/Catalog";
import ProductDetail from "./components/ProductDetail";
import TryOnCamera from "./components/TryOnCamera";

type View = "catalog" | "detail" | "camera";
export default function App() {
  const [products, setProducts] = useState<Product[]>([]);
  const [selected, setSelected] = useState<Product | null>(null);
  const [view, setView] = useState<View>("catalog");
  const [error, setError] = useState("");
  useEffect(() => {
    getProducts()
      .then(setProducts)
      .catch((e: Error) => setError(e.message));
  }, []);
  if (error)
    return (
      <main className="notice">No se pudo cargar el catálogo: {error}</main>
    );
  if (!products.length)
    return <main className="notice">Cargando catálogo…</main>;
  if (view === "camera" && selected)
    return <TryOnCamera product={selected} onClose={() => setView("detail")} />;
  if (view === "detail" && selected)
    return (
      <ProductDetail
        product={selected}
        onBack={() => setView("catalog")}
        onTry={() => setView("camera")}
      />
    );
  return (
    <Catalog
      products={products}
      onSelect={(product) => {
        setSelected(product);
        setView("detail");
      }}
    />
  );
}
