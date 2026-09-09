# Servicio que coordina todo el proceso de segmentación

from __future__ import annotations

import base64
import io
from PIL import Image
import httpx 

def prompt_for(product):
    return product.category.lower()


# Primero prioriza la confianza de SAM 3 y, si hay empate, prefiere la máscara de mayor área
def select_primary(candidates):
    return max(
        candidates,
        key=lambda candidate: (
            candidate.score,
            candidate.mask.getbbox()
            and (
                (candidate.mask.getbbox()[2] - candidate.mask.getbbox()[0])
                * (candidate.mask.getbbox()[3] - candidate.mask.getbbox()[1])
            )
            or 0
        )
    )
    

# Este método toma la imagen original + la máscara de SAM 3 y produce un PNG recortado donde solo 
# queda visible el objeto segmentado
def cutout(image_bytes: bytes, mask: Image.Image) -> tuple[bytes, int, int]:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    alpha = mask.resize(image.size).convert("L")
    image.putalpha(alpha)
    bbox = alpha.getbbox()
    if not bbox:
        raise ValueError("Selected mask is empty")
    result = image.crop(bbox)
    output = io.BytesIO()
    result.save(output, format="PNG", optimize=True)
    return output.getvalue(), result.width, result.height

   
async def download_image(url: str) -> bytes:
    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.content

    
async def generate_try_on(product, provider):
    source = await download_image(product.image_url)
    prompt = prompt_for(product)
    selected = select_primary(await provider.segment(source, prompt))
    png, width, height = cutout(source, selected.mask)
    return {
        "imageBase64": base64.b64encode(png).decode(),
        "width": width,
        "height": height,
        "prompt": prompt
    }
