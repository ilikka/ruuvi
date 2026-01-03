
CREATE SCHEMA IF NOT EXISTS ruuvi;

CREATE TABLE ruuvi.gateway (
    gw_mac TEXT PRIMARY KEY,
    name TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE ruuvi.sensor (
    tag_mac TEXT PRIMARY KEY,
    name TEXT,
    first_seen TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE ruuvi.data (
    id BIGSERIAL PRIMARY KEY,
    gw_mac TEXT NOT NULL,
    tag_mac TEXT NOT NULL,

    temperature REAL,
    humidity REAL,
    pressure REAL,
    battery REAL,
    rssi INTEGER,

    measured_at TIMESTAMPTZ DEFAULT now(),

    CONSTRAINT fk_gateway
        FOREIGN KEY (gw_mac) REFERENCES ruuvi.gateway (gw_mac),
    CONSTRAINT fk_sensor
        FOREIGN KEY (tag_mac) REFERENCES ruuvi.sensor (tag_mac)
);

CREATE TABLE ruuvi.raw (
    id BIGSERIAL PRIMARY KEY,
    gw_mac TEXT NOT NULL,
    tag_mac TEXT NOT NULL,

    raw_data TEXT NOT NULL,
    rssi INTEGER,

    received_at TIMESTAMPTZ DEFAULT now()
);




CREATE INDEX idx_measurement_tag_time
    ON ruuvi.data (tag_mac, measured_at DESC);

CREATE INDEX idx_measurement_gateway_time
    ON ruuvi.data (gw_mac, measured_at DESC);

CREATE INDEX idx_raw_tag_time
    ON ruuvi.raw (tag_mac, received_at DESC);

CREATE OR REPLACE VIEW ruuvi.v_sdata_with_sensor AS
SELECT
    d.id,
    d.gw_mac,
    d.tag_mac,
    s.name AS sensor_name,
    d.temperature,
    d.humidity,
    d.pressure,
    d.battery,
    d.rssi,
    d.measured_at
FROM ruuvi.data d
LEFT JOIN ruuvi.sensor s
  ON s.tag_mac = d.tag_mac
WHERE s.name <> 'Terassi' and s.name <> 'Ulkolämpötila' and s.name <> 'Lattia';

CREATE OR REPLACE VIEW ruuvi.v_udata_with_sensor AS
SELECT
    d.id,
    d.gw_mac,
    d.tag_mac,
    s.name AS sensor_name,
    d.temperature,
    d.humidity,
    d.pressure,
    d.battery,
    d.rssi,
    d.measured_at
FROM ruuvi.data d
LEFT JOIN ruuvi.sensor s
  ON s.tag_mac = d.tag_mac
WHERE s.name = 'Ulkolämpötila';

CREATE OR REPLACE VIEW ruuvi.v_sensor_battery AS
 SELECT d.id,
    d.gw_mac,
    d.tag_mac,
    s.name AS sensor_name,
    d.battery,
    d.rssi,
    d.measured_at
   FROM ruuvi.data d
     LEFT JOIN ruuvi.sensor s ON s.tag_mac = d.tag_mac
	 where d.battery <= '2.4'
	 and  s.name is not NULL;