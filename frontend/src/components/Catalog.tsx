import { Product } from '../api'
export default function Catalog({ products, onSelect }: { products: Product[]; onSelect(product: Product): void }) {
  return <main><header><span className="eyebrow">SDC · PUCP</span><h1>Casa <i>cerca</i></h1><p>Objetos que hacen espacio para ti.</p></header><section className="grid">{products.map(product => <button className="card" onClick={() => onSelect(product)} key={product.id}><img src={product.image_url} alt={product.name}/><span className="category">{product.category}</span><strong>{product.name}</strong><span>S/ {product.price}</span></button>)}</section></main>
}
