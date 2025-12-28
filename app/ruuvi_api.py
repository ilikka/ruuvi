# ruuvi_api.py
from fastapi import FastAPI, Request
# ßfrom ruuvi_decoders import decode_data as Decoder
from logging_config import setup_logging
import logging

import logging
import psycopg2
import os
import logging

# uvicorn ruuvi_api:app --host 0.0.0.0 --port 40064

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
decoder = Decoder()



@app.post("/ruuvi")
async def receive_ruuvi(request: Request):
    body = await request.json()
    logger.info("body : %s", body)    
    if "data" not in body:
        return {"error": "Invalid payload"}
    

    return {"status": "ok"}



