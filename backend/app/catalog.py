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


PRODUCTS = (
    Product("sillon-nordico", "Sillón Nórdico", "Sillón gris de una plaza con patas de madera.", 849, "sofa", "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=1200&q=85"),
    Product("silla-roble", "Silla de Roble", "Silla de comedor de madera clara y líneas minimalistas.", 289, "chair", "https://images.unsplash.com/photo-1750306956241-521124641c73?auto=format&fit=crop&fm=jpg&q=85&w=1200"),
    Product("lampara-arco", "Lámpara Arco", "Lámpara de pie metálica con pantalla de tela.", 399, "lamp", "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=1200&q=85"),
    Product("mesa-centro", "Mesa Centro Olmo", "Mesa de centro baja de madera maciza.", 559, "table", "https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?auto=format&fit=crop&w=1200&q=85"),
    Product("sofa-lino", "Sofa de Lino", "Sofa de tres plazas en lino beige con cojines suaves.", 1299, "sofa", "https://images.unsplash.com/photo-1540574163026-643ea20ade25?auto=format&fit=crop&w=1200&q=85"),
    Product("escritorio-nogal", "Escritorio Nogal", "Escritorio compacto de nogal para oficina en casa.", 679, "desk", "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?auto=format&fit=crop&w=1200&q=85"),
    Product("cama-aurora", "Cama Aurora", "Cama matrimonial tapizada con cabecera acolchada.", 1149, "bed", "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=85"),
    Product("estanteria-roble", "Estanteria de Roble", "Estanteria abierta de cinco niveles para libros y decoracion.", 499, "shelf", "https://images.unsplash.com/photo-1594620302200-9a762244a156?auto=format&fit=crop&w=1200&q=85"),
    Product("comoda-oliva", "Comoda Oliva", "Comoda de seis cajones con acabado verde oliva.", 729, "dresser", "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=1200&q=85"),
    Product("espejo-oval", "Espejo Oval", "Espejo de pared ovalado con marco de madera clara.", 219, "mirror", "https://images.unsplash.com/photo-1618220179428-22790b461013?auto=format&fit=crop&w=1200&q=85"),
    Product("alfombra-terra", "Alfombra Terra", "Alfombra tejida de tonos tierra para sala o dormitorio.", 179, "rug", "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1200&q=85"),
    Product("gabinete-siena", "Gabinete Siena", "Gabinete bajo con puertas de rejilla para almacenamiento.", 639, "cabinet", "https://images.unsplash.com/photo-1558997519-83ea9252edf8?auto=format&fit=crop&w=1200&q=85"),
    Product("taburete-olmo", "Taburete Olmo", "Taburete alto de madera para barra de cocina.", 159, "stool", "https://images.unsplash.com/photo-1524758631624-e2822e304c36?auto=format&fit=crop&w=1200&q=85"),
    Product("banco-cedro", "Banco Cedro", "Banco de entrada de cedro macizo con diseno minimalista.", 349, "bench", "https://images.unsplash.com/photo-1551298370-9d3d53740c72?auto=format&fit=crop&w=1200&q=85"),
    Product("puf-boucle", "Puf Boucle", "Puf redondo tapizado en boucle color crema.", 189, "ottoman", "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=1200&q=85"),
    Product("biblioteca-linea", "Biblioteca Linea", "Biblioteca alta de metal negro y madera natural.", 579, "bookcase", "https://images.unsplash.com/photo-1507842217343-583bb7270b66?auto=format&fit=crop&w=1200&q=85"),
    Product("armario-nube", "Armario Nube", "Armario de dos puertas con amplio espacio interior.", 899, "wardrobe", "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=1200&q=85"),
    Product("mesita-noche", "Mesita de Noche", "Mesa auxiliar con cajon y tirador de laton.", 249, "nightstand", "https://images.unsplash.com/photo-1532323544230-7191fd51bc1b?auto=format&fit=crop&w=1200&q=85"),
    Product("aparador-miel", "Aparador Miel", "Aparador de madera con tres puertas para comedor.", 779, "sideboard", "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=1200&q=85"),
    Product("consola-nordica", "Consola Nordica", "Consola angosta de recibidor con cubierta de roble.", 429, "console", "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=1200&q=85"),
)


def get_product(product_id):
    for product in PRODUCTS:
        if product.id == product_id:
            return product
        
    return None