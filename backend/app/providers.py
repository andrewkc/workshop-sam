"""Segmentation adapters. Gateways normalize their response before returning candidates."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
import base64
import io
import os
from PIL import Image, ImageDraw
import httpx


@dataclass
class MaskCandidate:
    mask: Image.Image
    score: float


class SegmentationProvider(ABC):
    @abstractmethod
    async def segment(self, image_bytes: bytes, prompt: str) -> list[MaskCandidate]: ...


class DemoProvider(SegmentationProvider):
    """Deterministic fallback mask for workshop continuity; not ML segmentation."""
    async def segment(self, image_bytes: bytes, prompt: str) -> list[MaskCandidate]:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        width, height = image.size
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        # A centered, softly rounded subject-shaped region makes the full UI demoable offline.
        margin_x, margin_y = int(width * .13), int(height * .07)
        draw.rounded_rectangle((margin_x, margin_y, width - margin_x, height - int(height * .03)), radius=int(min(width, height) * .08), fill=255)
        return [MaskCandidate(mask, .5)]


class HttpSam3Provider(SegmentationProvider):
    """Adapter contract: POST multipart image,prompt; response {masks:[{png_base64,score}]}."""
    def __init__(self, url: str, api_key: str):
        self.url, self.api_key = url, api_key

    async def segment(self, image_bytes: bytes, prompt: str) -> list[MaskCandidate]:
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        files = {"image": ("product.jpg", image_bytes, "image/jpeg")}
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(self.url, headers=headers, data={"prompt": prompt}, files=files)
            response.raise_for_status()
        payload = response.json()
        candidates = []
        for item in payload.get("masks", []):
            raw = base64.b64decode(item["png_base64"])
            candidates.append(MaskCandidate(Image.open(io.BytesIO(raw)).convert("L"), float(item.get("score", 0))))
        if not candidates:
            raise ValueError("SAM 3 gateway returned no masks")
        return candidates


def provider_from_env() -> SegmentationProvider:
    provider = os.getenv("SEGMENTATION_PROVIDER", "demo").lower()
    url, key = os.getenv("SAM3_API_URL", ""), os.getenv("SAM3_API_KEY", "")
    if provider == "sam3" and url:
        return HttpSam3Provider(url, key)
    if os.getenv("DEMO_MASKS_ENABLED", "true").lower() == "true":
        return DemoProvider()
    raise RuntimeError("No segmentation provider configured")
