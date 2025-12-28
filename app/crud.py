from sqlalchemy.orm import Session
from models import Gateway, Sensor, Data, Raw

def get_or_create_gateway(db: Session, gw_mac: str):
  gateway = db.query(Gateway).filter_by(gw_mac=gw_mac).first()
  if not gateway:
      gateway = Gateway(gw_mac=gw_mac)
      db.add(gateway)
      db.commit()
  return gateway

def get_or_create_sensor(db: Session, tag_mac: str):
  sensor = db.query(Sensor).filter_by(tag_mac=tag_mac).first()
  if not sensor:
    sensor = Sensor(tag_mac=tag_mac)
    db.add(sensor)
    db.commit()
  return sensor

def save_raw(db: Session, gw_mac, tag_mac, raw_data, rssi):
  raw = Raw(gw_mac=gw_mac, tag_mac=tag_mac, raw_data=raw_data, rssi=rssi)
  db.add(raw)
  db.commit()
  return raw

def save_data(db: Session, gw_mac, tag_mac, temperature=None, humidity=None, pressure=None, battery=None, rssi=None):
  data = Data(
    gw_mac=gw_mac,
    tag_mac=tag_mac,
    temperature=temperature,
    humidity=humidity,
    pressure=pressure,
    battery=battery,
    rssi=rssi
  )
  db.add(data)
  db.commit()
  return data
