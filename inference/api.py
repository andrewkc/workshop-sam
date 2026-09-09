from fastapi import FastAPI, UploadFile, File, Form
from PIL import Image
from io import BytesIO

from model import segment

app = FastAPI()

@app.post("/segment")
async def segment_endpoint(
    image: UploadFile = File(...),
    prompt: str = Form(...)
):
    image_data = await image.read()
    image = Image.open(BytesIO(image_data)).convert("RGB")

    masks = segment(image, prompt)

    return {
        "masks": masks
    }