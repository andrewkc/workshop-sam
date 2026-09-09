from transformers import Sam3Model, Sam3Processor
import torch
import base64
import io
from PIL import Image

model = Sam3Model.from_pretrained(
    "facebook/sam3",
    device_map="auto"
)

processor = Sam3Processor.from_pretrained("facebook/sam3")

def mask_to_base64(mask):
    mask = mask.cpu().numpy().astype("uint8") * 255

    image = Image.fromarray(mask, mode="L")

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")

    return base64.b64encode(buffer.getvalue()).decode()

def segment(image, prompt):
    inputs = processor(
        images=image,
        text=prompt,
        return_tensors="pt"
    ).to(model.device)

    with torch.no_grad():
        outputs = model(**inputs)

    results = processor.post_process_instance_segmentation(
        outputs,
        threshold=0.5,
        mask_threshold=0.5,
        target_sizes=inputs.get("original_sizes").tolist()
    )[0]

    masks = []

    for mask, score in zip(results["masks"], results["scores"]):
        masks.append({
            "png_base64": mask_to_base64(mask),
            "score": float(score)
        })

    return masks