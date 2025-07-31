from .database import user_collection
from bson import ObjectId

# Function to create a new user in the database
async def create_user(user: dict):
    await user_collection.insert_one(user)
    return user["user_id"]

# Function to get a user by email
async def get_user_by_email(email: str):
    return await user_collection.find_one({"email": email})

# Function to get a user by ID
async def get_user_by_id(user_id: str):
    return await user_collection.find_one({"user_id": user_id})