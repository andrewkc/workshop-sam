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


class HttpSam3Provider():
    # Adapter contract: POST multipart image,prompt response {masks:[{png_base64,score}]}
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

def provider_from_env():
    provider = os.getenv("SEGMENTATION_PROVIDER", "").lower()
    url, key = os.getenv("SAM3_API_URL", ""), os.getenv("SAM3_API_KEY", "")
    if provider == "sam3" and url:
        return HttpSam3Provider(url, key)
    raise RuntimeError("No segmentation provider configured")
