from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument

class CounterRepository:
    """Repository for managing atomic counters in MongoDB."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    def get_next_sequence(self, key: str) -> int:
        """Retrieves and increments the counter for a given key (e.g., 'employee_invoice')."""
        result = self.db.counters.find_one_and_update(
            {"_id": key},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        return result["seq"]
