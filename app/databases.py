
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

MONGODB_URL = config("MONGODB_URL")

client = AsyncIOMotorClient(MONGODB_URL)
database = client.barbers

def get_database():
    return database