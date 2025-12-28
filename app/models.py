from sqlalchemy import Column, String, Integer, BigInteger, Float, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Gateway(Base):
    __tablename__ = "gateway"
    __table_args__ = {"schema": "ruuvi"}

    gw_mac = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class Sensor(Base):
    __tablename__ = "sensor"
    __table_args__ = {"schema": "ruuvi"}

    tag_mac = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    first_seen = Column(TIMESTAMP(timezone=True), server_default=func.now())

class Data(Base):
    __tablename__ = "data"
    __table_args__ = {"schema": "ruuvi"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    gw_mac = Column(String, ForeignKey("ruuvi.gateway.gw_mac"), nullable=False)
    tag_mac = Column(String, ForeignKey("ruuvi.sensor.tag_mac"), nullable=False)
    temperature = Column(Float)
    humidity = Column(Float)
    pressure = Column(Float)
    battery = Column(Float)
    rssi = Column(Integer)
    measured_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class Raw(Base):
    __tablename__ = "raw"
    __table_args__ = {"schema": "ruuvi"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    gw_mac = Column(String, nullable=False)
    tag_mac = Column(String, nullable=False)
    raw_data = Column(Text, nullable=False)
    rssi = Column(Integer)
    received_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
