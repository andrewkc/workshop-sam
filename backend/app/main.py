from __future__ import annotations

import os

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .catalog import PRODUCTS, get_product
from .image_service import generate_try_on 
from .providers import provider_from_env

app = FastAPI(title="Marketplace Vision AI")
origins = [item.strip() for item in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/api/health")
async def health():
    return {"ok": True}

@app.get("/api/products")
async def products():
    return [product.to_dict() for product in PRODUCTS]

@app.post("/api/products/{product_id}/try-on")
async def try_on(product_id):
    print("DEBUG 1", product_id)
    product = get_product(product_id)
    print("DEBUG 2", product.to_dict())
    if not product:
        raise HTTPException(404, "Producto no encontrado")
    
    try:
        result = await generate_try_on(product, provider_from_env())
        return result
    except Exception as exc:
        raise Exception(502, f"No se pudo segmentar el producto: {exc}") from exc
