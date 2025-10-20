from motor.motor_asyncio import AsyncIOMotorDatabase

class CounterRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    def get_next_sequence(self, key: str) -> int:
        """
        Recupera e incrementa o contador para a chave (ex: 'employee_invoice').
        Deve ser transacional/atômico no DB ou Redis.
        """
        result = self.db.counters.find_one_and_update(
            {"_id": key},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=True
        )
        return result["seq"]
