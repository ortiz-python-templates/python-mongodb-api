from src.common.config.db_config import DbConfig

# Get default DB from env config
db = DbConfig.get_database()

# Access a collection
users_collection = db['users']

# Example: insert a document
import asyncio

async def add_user():
    result = await users_collection.insert_one({"name": "John Doe", "email": "john@example.com"})
    print("Inserted ID:", result.inserted_id)

asyncio.run(add_user())
