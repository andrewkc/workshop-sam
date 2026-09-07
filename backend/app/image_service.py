from __future__ import annotations

import base64
import io
from PIL import Image, ImageChops
import httpx
from .providers import MaskCandidate, SegmentationProvider


def prompt_for(product) -> str:
    # SAM 3 concept prompts work best as concise noun phrases.
    return f"{product.category} {product.name}".lower()


def select_primary(candidates: list[MaskCandidate]) -> MaskCandidate:
    return max(candidates, key=lambda candidate: (candidate.score, candidate.mask.getbbox() and (candidate.mask.getbbox()[2] - candidate.mask.getbbox()[0]) * (candidate.mask.getbbox()[3] - candidate.mask.getbbox()[1]) or 0))


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


async def generate_try_on(product, provider: SegmentationProvider) -> dict:
    source = await download_image(product.image_url)
    prompt = prompt_for(product)
    selected = select_primary(await provider.segment(source, prompt))
    png, width, height = cutout(source, selected.mask)
    return {"imageBase64": base64.b64encode(png).decode(), "width": width, "height": height, "prompt": prompt, "cached": False}
