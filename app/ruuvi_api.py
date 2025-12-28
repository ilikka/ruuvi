# ruuvi_api.py

"""
FastAPI application for receiving Ruuvi Gateway push messages.
"""


# from ruuvi_decoders import decode_data as Decoder
import logging
# import psycopg2
# import os

from fastapi import FastAPI, Request

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/ruuvi")
async def receive_ruuvi(request: Request):
    """
    Docstring for receive_ruuvi
    
    :param request: value of sensors
    :type request: Post Request
    """

    body = await request.json()
    logger.info("body : %s", body)

    if "data" not in body:
        logger.warning("Invalid payload: %s", body)
        return {"error": "Invalid payload"}

    return {"status": "ok"}
