# config.py
"""
secrets for ruuvi app
"""
from decouple import config

DATABASE_URL = config(
    "DATABASE_URL",
    default="postgresql://user:password@localhost:5432/ruuvi"
)

API_KEY = config(
    "API_KEY",
    default="mysecretapikey"
)
