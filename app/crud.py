"""
save data from ruuvi gateway to database
"""
from sqlalchemy.orm import Session 
from sqlalchemy  import func 
from models import Gateway, Sensor, Data, Raw

def get_or_create_gateway(db: Session, gw_mac: str):
  """
  Docstring for get_or_create_gateway
  
  :param db: Database session
  :type db: Session
  :param gw_mac: ruuvi gateway MAC address
  :type gw_mac: str
  """
  gateway = db.query(Gateway).filter_by(gw_mac=gw_mac).first()
  if not gateway:
    gateway = Gateway(gw_mac=gw_mac)
    db.add(gateway)
    db.commit()
  return gateway

def get_or_create_sensor(db: Session, tag_mac: str):
  """
  Docstring for get_or_create_sensor
  
  :param db: Database session
  :type db: Session
  :param tag_mac: sensors MAC address 
  :type tag_mac: str
  """
  sensor = db.query(Sensor).filter_by(tag_mac=tag_mac).first()
  if not sensor:
    sensor = Sensor(tag_mac=tag_mac)
    db.add(sensor)
    db.commit()
  return sensor

def save_raw(db: Session, gw_mac, tag_mac, raw_data, rssi):
  """
  Docstring for save_raw
  
  :param db: db
  :type db: Session
  :param gw_mac: ruuvi gateway MAC address
  :param tag_mac: sensors MAC address
  :param raw_data: if used
  :param rssi: signal strength
  """
  raw = Raw(gw_mac=gw_mac, tag_mac=tag_mac, raw_data=raw_data, rssi=rssi)
  db.add(raw)
  db.commit()
  return raw

def save_data(db: Session, gw_mac, tag_mac, temperature=None, humidity=None, pressure=None, battery=None, rssi=None, timestamp=None):
  """
  Docstring for save formatted data
  :param db: db
  :type db: Session
  :param gw_mac: ruuvi gateway MAC address
  :param tag_mac: sensors MAC address
  :param temperature: temperature value
  :param humidity: humidity value
  :param pressure: pressure value
  :param battery: battery voltage
  :param rssi: signal strength
  :param timestamp: measurement timestamp from sensor

  """
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


def get_max_id_by_gw_mac(db, gw_mac: str) -> int:
    """
    Docstring for get_max_id_by_gw_mac
    
    :param db: Description
    :param gw_mac: Description
    :type gw_mac: str
    :return: Description
    :rtype: int
    """
    # Check if gateway exists
    gateway_exists = db.query(Gateway).filter(Gateway.gw_mac == gw_mac).first()

    if not gateway_exists:
        return 0

    #  Get max id from data table
    max_id = db.query(func.max(Data.id))\
        .filter(Data.gw_mac == gw_mac)\
        .scalar()

    return max_id or 0
