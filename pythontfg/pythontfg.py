import hmac
import hashlib
import reflex as rx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from reflex.utils.types import ASGIApp

from . import styles
from .pages import *

# Tu token de verificación (debe coincidir con el configurado en el Dashboard de Meta)
VERIFY_TOKEN = "IGAAJjZCgJaBSxBZAFA2OWJHWjQ4YTdBQXRCV3J3RUVpSjVreWNUYnNmRjVYOWRXbE1UbU4tb19CdWVzNFdzRFRORDJTMFZAwckxzb0d2YWtIS05KZAmlSNktjbkJkaFh6ME9RbkpxTDR3V3RRTWxfakRCNTI3OUJ2Vm5VTGtydzhPTQZDZD"
# Tu App Secret (lo obtienes en el Dashboard de Meta)
APP_SECRET = "ddfcf743faff99625926127375107e41"

fastapi_app = FastAPI(title="api")

@fastapi_app.get("/api/items")
async def get_items():
    """Endpoint para obtener la lista de ítems."""
    return {"items": ["Item1", "Item2", "Item3"]}

# --- Webhook de Instagram ---

@fastapi_app.get("/instagram/webhook")
async def instagram_verify(
    hub_mode: str | None = None,
    hub_verify_token: str | None = None,
    hub_challenge: str | None = None):
    """
    Verificación inicial de Instagram:
    Debe responder con hub.challenge si el token coincide.
    """
    # Debug: imprime lo que llega
    print(f"[VERIFY] mode={hub_mode!r}, token_in={hub_verify_token!r}, expected={VERIFY_TOKEN!r}")
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(hub_challenge or "", status_code=200)
    raise HTTPException(status_code=403, detail="Token de verificación inválido")

@fastapi_app.post("/instagram/webhook")
async def instagram_webhook(request: Request):
    """
    Recepción de eventos de Instagram:
    1) Valida la firma HMAC-SHA256
    2) Procesa el JSON si la firma es correcta
    """
    raw_body = await request.body()
    signature_header = request.headers.get("X-Hub-Signature-256", "")
    # signature_header tiene formato "sha256=<hash>"
    try:
        prefix, signature = signature_header.split("=", 1)
    except ValueError:
        raise HTTPException(status_code=400, detail="Header de firma mal formado")

    # Calcula HMAC-SHA256 del cuerpo con tu APP_SECRET
    expected_hmac = hmac.new(
        key=APP_SECRET.encode("utf-8"),
        msg=raw_body,
        digestmod=hashlib.sha256
    ).hexdigest()

    # Comparación segura (para evitar timing attacks)
    if not hmac.compare_digest(expected_hmac, signature):
        print(f"[WEBHOOK] Firma inválida: recibida={signature!r}, esperada={expected_hmac!r}")
        raise HTTPException(status_code=400, detail="Firma HMAC inválida")

    # Si la firma es correcta, parsea y procesa el JSON
    payload = await request.json()
    print("Evento Instagram recibido:", payload)
    return JSONResponse({"status": "received"}, status_code=200)

# --------------------------

def transformer(asgi_app: ASGIApp) -> ASGIApp:
    """
    Monta la app de Reflex en FastAPI.
    FastAPI maneja primero /api y /instagram/webhook;
    todo lo demás se delega a Reflex.
    """
    fastapi_app.mount("", asgi_app)
    return fastapi_app

# Inicializa la app de Reflex usando el transformer
app = rx.App(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
    api_transformer=transformer,
)
