from decouple import config

DATABASE_URL = config("DATABASE_URL", default="postgresql+asyncpg://user:password@localhost:5432/ruuvi")
