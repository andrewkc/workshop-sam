from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class Product:
    id: str
    name: str
    description: str
    price: int
    category: str
    image_url: str

    def public(self):
        return asdict(self)


# Unsplash Source images are used only as workshop placeholders. Replace with licensed assets.
PRODUCTS = (
    Product("sillon-nordico", "Sillón Nórdico", "Sillón gris de una plaza con patas de madera.", 849, "sillón", "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=1200&q=85"),
    Product("silla-roble", "Silla de Roble", "Silla de comedor de madera clara y líneas minimalistas.", 289, "silla", "https://images.unsplash.com/photo-1503602642458-232111445657?auto=format&fit=crop&w=1200&q=85"),
    Product("lampara-arco", "Lámpara Arco", "Lámpara de pie metálica con pantalla de tela.", 399, "lámpara", "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=1200&q=85"),
    Product("mesa-centro", "Mesa Centro Olmo", "Mesa de centro baja de madera maciza.", 559, "mesa de centro", "https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?auto=format&fit=crop&w=1200&q=85"),
)


def get_product(product_id: str) -> Product | None:
    return next((product for product in PRODUCTS if product.id == product_id), None)
