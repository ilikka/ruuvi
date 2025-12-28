from fastapi import FastAPI, Request, Depends
import logging
import asyncio
from sqlalchemy.orm import Session

from database import get_db
import crud

logger = logging.getLogger("ruuvi")
logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title="Ruuvi API")

@app.post("/ruuvi")
async def receive_ruuvi(request: Request, db: Session = Depends(get_db)):
  body = await request.json()
  logger.debug("Received payload: %s", body)

  if "tag_mac" not in body:
    logger.warning("Invalid payload: %s", body)
    return {"error": "Invalid payload"}


  gw_mac = body.get("gw_mac")
  tag_mac = body.get("tag_mac")
  rssi = body.get("rssi")
  raw_data = body.get("raw_data")
  temperature = body.get("temperature")
  humidity = body.get("humidity")
  pressure = body.get("pressure")
  battery = body.get("battery")

  if not gw_mac or not tag_mac:
    return {"error": "Missing gw_mac or tag_mac"}

  # Run synchronous DB calls in a thread to avoid async errors
  await asyncio.to_thread(crud.get_or_create_gateway, db, gw_mac)
  await asyncio.to_thread(crud.get_or_create_sensor, db, tag_mac)
  await asyncio.to_thread(crud.save_raw, db, gw_mac, tag_mac, raw_data, rssi)
  await asyncio.to_thread(crud.save_data, db, gw_mac, tag_mac, temperature, humidity, pressure, battery, rssi)

  return {"status": "ok"}
