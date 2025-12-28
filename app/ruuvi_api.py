from fastapi import FastAPI, Request, Depends, HTTPException
import logging
import asyncio
from sqlalchemy.orm import Session

from config import API_KEY
from database import get_db
import crud

logger = logging.getLogger("ruuvi")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Ruuvi API")


def verify_api_key(request: Request):
  auth = request.headers.get("Authorization")
  logger.debug("Received auth: %s", auth)
  if not auth or auth != f"Bearer {API_KEY}":
    raise HTTPException(status_code=401, detail="Invalid API Key")



@app.post("/ruuvi")
async def receive_ruuvi(
  request: Request, 
  db: Session = Depends(get_db), 
  _=Depends(verify_api_key)): # underscore signals "unused"

  body = await request.json()
  logger.debug("Received payload: %s", body)

  data = body.get("data", {})
  gw_mac = data.get("gw_mac")
  tags = data.get("tags", [])
    
  if not gw_mac or not tags:
    logger.warning("Invalid payload: %s", body)
    return {"error": "Invalid payload"}


  for tag_mac, tag_data in tags.items():
    rssi = tag_data.get("rssi")
    temperature = tag_data.get("temperature")
    humidity = tag_data.get("humidity")
    pressure = tag_data.get("pressure")
    voltage = tag_data.get("voltage")

    logger.debug(
      "gw=%s tag=%s temp=%.2f hum=%.2f",
      gw_mac, tag_mac, temperature, humidity
    )

    # Run synchronous DB calls in a thread to avoid async errors
    await asyncio.to_thread(crud.get_or_create_gateway, db, gw_mac)
    await asyncio.to_thread(crud.get_or_create_sensor, db, tag_mac)
    await asyncio.to_thread(crud.save_data, db, gw_mac, tag_mac, temperature, humidity, pressure, voltage, rssi)



  

  # await asyncio.to_thread(crud.save_raw, db, gw_mac, tag_mac, raw_data, rssi)
  
  return {"status": "ok"}
