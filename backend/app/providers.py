import base64
import io
import os

import httpx
from PIL import Image

class HttpSam3Provider:
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key
    
    async def segment(self, image_bytes, prompt):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        files = {
            "image": ("product.jpg", image_bytes, "image/jpeg")
        }
        
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(
                self.url,
                headers=headers,
                data={"prompt": prompt},
                files=files
            )
            
        response.raise_for_status()
        payload = response.json()
        
        candidates = []
        
        for item in payload["masks"]:
            
            mask_bytes = base64.b64decode(item["png_base64"])
            mask = Image.open(io.BytesIO(mask_bytes)).convert("L")
            
            candidates.append(
                {
                    "mask": mask,
                    "score": item["score"]
                }

            ) 
        return candidates

def provider_from_env():
    
    url = os.getenv("SAM3_API_URL")
    key = os.getenv("SAM3_API_KEY")
    return HttpSam3Provider(url, key)