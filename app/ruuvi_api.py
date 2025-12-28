# ruuvi_api.py
from fastapi import FastAPI, Request
from ruuvi_decoders import Decoder
import logging
import psycopg2
import os

app = FastAPI()
decoder = Decoder()

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=os.environ.get("PG_HOST", "localhost"),
    dbname=os.environ.get("PG_DB", "ruuvi"),
    user=os.environ.get("PG_USER", "ruuvi_user"),
    password=os.environ.get("PG_PASS", "secret")
)
cur = conn.cursor()

@app.post("/ruuvi")
async def receive_ruuvi(request: Request):
    body = await request.json()
    
    if "data" not in body:
        return {"error": "Invalid payload"}
    
    gw_mac = body["data"].get("gwmac", "")
    tags = body["data"].get("tags", {})

    for tag_mac, tag in tags.items():
        rssi = tag.get("rssi")
        raw_data = tag.get("data", "")
        
        # Decode Ruuvi sensor data
        try:
            decoded = decoder.decode_raw(raw_data)
        except Exception:
            decoded = {}
        
        temperature = decoded.get("temperature")
        humidity = decoded.get("humidity")
        pressure = decoded.get("pressure")
        battery = decoded.get("battery")
            
        # Insert into PostgreSQL
        cur.execute("""
            INSERT INTO ruuvi_data(gw_mac, tag_mac, temperature, humidity, pressure, battery, rssi)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (gw_mac, tag_mac, temperature, humidity, pressure, battery, rssi))
        
    conn.commit()
    return {"status": "ok"}
