from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class Product:
    id: str
    name: str
    description: str
    price: int
    category: str
    image_url: str

    def to_dict(self):
        return asdict(self)


PRODUCTS = (
    Product("sillon-nordico", "Sillón Nórdico", "Sillón gris de una plaza con patas de madera.", 849, "sofa", "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=1200&q=85"), #
    Product("silla-roble", "Silla de Roble", "Silla de comedor de madera clara y líneas minimalistas.", 289, "chair", "https://images.unsplash.com/photo-1750306956241-521124641c73?auto=format&fit=crop&fm=jpg&q=85&w=1200"), #
    Product("lampara-arco", "Lámpara Arco", "Lámpara de pie metálica con pantalla de tela.", 399, "lamp", "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=1200&q=85"), #
    Product("mesa-centro", "Mesa Centro Olmo", "Mesa de centro baja de madera maciza.", 559, "table", "https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?auto=format&fit=crop&w=1200&q=85"), #
    Product("sofa-lino", "Sofa de Lino", "Sofa de tres plazas en lino beige con cojines suaves.", 1299, "sofa", "https://images.unsplash.com/photo-1540574163026-643ea20ade25?auto=format&fit=crop&w=1200&q=85"), #
    Product("gabinete-siena", "Gabinete Siena", "Gabinete bajo con puertas de rejilla para almacenamiento.", 639, "cabinet", "https://images.unsplash.com/photo-1558997519-83ea9252edf8?auto=format&fit=crop&w=1200&q=85"), #
    Product("cama-aurora", "Cama Aurora", "Cama matrimonial tapizada con cabecera acolchada.", 1149, "bed and pillows", "https://www.saatva.com/blog/wp-content/uploads/2023/07/how-to-arrange-pillows-on-a-bed-1.jpg"), #
    Product("espejo-rectangular", "Espejo Rectangular", "Espejo de pared rectangular con marco de madera clara.", 219, "mirror", "https://promart.vteximg.com.br/arquivos/ids/10755975-1000-1000/149408.jpg?v=639150743890430000") # 
)


def get_product(product_id):
    for product in PRODUCTS:
        if product.id == product_id:
            return product
        
    return None