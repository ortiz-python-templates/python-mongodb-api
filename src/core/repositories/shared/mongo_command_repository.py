from typing import Dict, TypeVar, Generic, List, Optional, Type, Any, Union
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection


T = TypeVar('T', bound=BaseModel)

class MongoCommandRepository(Generic[T]):

    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str, model_cls: Type[T]):
        self._database = db
        self.collection: AsyncIOMotorCollection = db[collection_name]
        self.model_cls = model_cls
        self.inserted_id: Optional[Any] = None

    
    # Create
    async def create(self, entity: T, session=None):
        result = await self.collection.insert_one(entity.model_dump(), session=session)
        self.inserted_id = result.inserted_id
        return self.inserted_id

    async def create_batch(self, entities: List[T], session=None):
        await self.collection.insert_many([e.model_dump() for e in entities], session=session)

    
    # Update
    async def update(self, id: ObjectId, entity: T, session=None):
        await self.collection.replace_one({"_id": id}, entity.model_dump(), session=session)

    async def update_batch(self, entities: List[T], session=None):
        for entity in entities:
            await self.collection.replace_one({"_id": entity.id}, entity.model_dump(), session=session)
    
    async def update_raw(self, filter: Dict[str, Any], update: Dict[str, Any], upsert=False, session=None):
        result = await self.collection.update_many(
            filter,
            update,
            upsert=upsert,
            session=session
        )
        return result

    
    # Hard delete
    async def delete(self, id: ObjectId, session=None):
        await self.collection.delete_one({"_id": id}, session=session)

    async def delete_by_field(self, field: str, value: Any, session=None):
        await self.collection.delete_one({field: value}, session=session)
    

    # Soft delete
    async def soft_delete(self, unique_id: str, deleted_by: Optional[str] = None, session=None):
        """
        Soft delete a document by setting `is_deleted=True` and recording deleted_by / deleted_at
        """
        await self.collection.update_one(
            {"unique_id": unique_id, "is_deleted": False},
            {"$set": {
                "is_deleted": True,
                "deleted_at": datetime.utcnow(),
                "deleted_by": deleted_by
            }},
            session=session
        )

    # Increase and decrease
    async def increase_value(self, id: ObjectId, field: str, value: Union[int, float]):
        update = {"$inc": {field: value}}
        result = await self.collection.update_one({"_id": id, "is_deleted": False}, update)
        return result.modified_count

    async def decrease_value(self, id: ObjectId, field: str, value: Union[int, float]):
        update = {"$inc": {field: -value}}
        result = await self.collection.update_one({"_id": id, "is_deleted": False}, update)
        return result.modified_count
    
    
    # Auxiliary Queries
    async def get_by_field_aux(self, field: str, value: Any) -> Optional[T]:
        doc = await self.collection.find_one({field: value, "is_deleted": False})
        return self.model_cls.model_validate(doc) if doc else None
    
    async def get_by_id_aux(self, id: ObjectId) -> Optional[T]:
        return await self.get_by_field_aux('_id', id)

    async def get_by_unique_id_aux(self, unique_id: str) -> Optional[T]:
        return await self.get_by_field_aux('unique_id', unique_id)

    async def get_last_aux(self) -> Optional[T]:
        doc = await self.collection.find_one({"is_deleted": False}, sort=[("_id", -1)])
        return self.model_cls.model_validate(doc) if doc else None

    async def get_first_aux(self) -> Optional[T]:
        doc = await self.collection.find_one({"is_deleted": False}, sort=[("_id", 1)])
        return self.model_cls.model_validate(doc) if doc else None

    async def exists_record(self, field: str, value: Any) -> bool:
        count = await self.collection.count_documents({field: value, "is_deleted": False})
        return count > 0

    async def exists_excluding_id(self, unique_id: str, filters: dict) -> bool:
        or_conditions = [{k: v} for k, v in filters.items()]
        query = {"unique_id": {"$ne": unique_id}, "$or": or_conditions, "is_deleted": False}
        count = await self.collection.count_documents(query)
        return count > 0
