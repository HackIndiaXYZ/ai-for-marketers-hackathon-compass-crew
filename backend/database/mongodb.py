import os
from datetime import datetime
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from bson import ObjectId

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = "pain2ad"

client: Optional[AsyncIOMotorClient] = None
db: Optional[AsyncIOMotorDatabase] = None


async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    await create_indexes()
    print(f"Connected to MongoDB: {DATABASE_NAME}")


async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("MongoDB connection closed")


def get_database() -> AsyncIOMotorDatabase:
    if db is None:
        raise RuntimeError("Database not initialized. Call connect_to_mongo first.")
    return db


async def create_indexes():
    database = get_database()

    await database.users.create_index("email", unique=True)

    await database.analyses.create_index("user_id")
    await database.analyses.create_index("status")

    await database.pain_points.create_index("analysis_id")

    await database.personas.create_index("analysis_id")

    await database.ad_assets.create_index("analysis_id")
    await database.ad_assets.create_index("persona_id")

    await database.campaigns.create_index("user_id")

    await database.competitors.create_index("analysis_id")


def serialize_doc(doc: Optional[dict]) -> Optional[dict]:
    if doc is None:
        return None
    serialized = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            serialized[key] = str(value)
        elif isinstance(value, datetime):
            serialized[key] = value.isoformat()
        else:
            serialized[key] = value
    if "_id" in serialized:
        serialized["id"] = serialized.pop("_id")
    return serialized


def serialize_docs(docs: list) -> list:
    return [serialize_doc(doc) for doc in docs]


async def get_collection(name: str):
    database = get_database()
    return database[name]
