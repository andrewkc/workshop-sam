import { Product } from '../api'
export default function ProductDetail({ product, onBack, onTry }: { product: Product; onBack(): void; onTry(): void }) {
 return <main><button className="back" onClick={onBack}>← Catálogo</button><section className="detail"><img src={product.image_url} alt={product.name}/><div><span className="category">{product.category}</span><h1>{product.name}</h1><h2>S/ {product.price}</h2><p>{product.description}</p><button className="primary" onClick={onTry}>⌁ Probar en mi espacio</button><small>Usaremos tu cámara solo mientras pruebas el producto.</small></div></section></main>
}
