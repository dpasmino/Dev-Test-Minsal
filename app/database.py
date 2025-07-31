from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
import os

# MongoDB connection URL
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://mongo:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client["userdb"]
user_collection = db["users"]

# Index for email uniqueness
user_collection.create_index([("email", ASCENDING)], unique=True)