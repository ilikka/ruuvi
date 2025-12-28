# app/main_sync.py
from fastapi import FastAPI, Request, Depends
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Gateway, Sensor, Data, Raw
from config import DATABASE_URL

# Sync engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

logger = logging.getLogger("ruuvi")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Ruuvi API (Sync)")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/ruuvi")
def receive_ruuvi(request: Request, db=Depends(get_db)):
    body = await request.json()
    logger.info("Received: %s", body)

    if "data" not in body:
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

    # Insert gateway if not exists
    if not db.query(Gateway).filter_by(gw_mac=gw_mac).first():
        db.add(Gateway(gw_mac=gw_mac))
        db.commit()

    # Insert sensor if not exists
    if not db.query(Sensor).filter_by(tag_mac=tag_mac).first():
        db.add(Sensor(tag_mac=tag_mac))
        db.commit()

    # Save raw data
    db.add(Raw(gw_mac=gw_mac, tag_mac=tag_mac, raw_data=raw_data, rssi=rssi))
    # Save decoded data
    db.add(Data(
        gw_mac=gw_mac,
        tag_mac=tag_mac,
        temperature=temperature,
        humidity=humidity,
        pressure=pressure,
        battery=battery,
        rssi=rssi
    ))
    db.commit()

    return {"status": "ok"}
