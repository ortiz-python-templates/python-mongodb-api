from typing import TypeVar, Generic, List, Optional, Type, Any
from bson import ObjectId
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

T = TypeVar('T', bound=BaseModel)


class MongoCommandRepository(Generic[T]):

    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str, model_cls: Type[T]):
        self._database = db
        self._collection: AsyncIOMotorCollection = db[collection_name]
        self._model_cls = model_cls
        self.inserted_id: Optional[Any] = None

    async def create(self, entity: T, session=None):
        result = await self._collection.insert_one(entity.model_dump(), session=session)
        self.inserted_id = result.inserted_id
        return self.inserted_id

    async def create_batch(self, entities: List[T], session=None):
        await self._collection.insert_many([e.model_dump() for e in entities], session=session)

    async def delete(self, id: ObjectId, session=None):
        await self._collection.delete_one({"_id": id}, session=session)

    async def delete_by_field(self, field: str, value: Any, session=None):
        await self._collection.delete_one({field: value}, session=session)

    async def update(self, id: ObjectId, entity: T, session=None):
        await self._collection.replace_one({"_id": id}, entity.model_dump(), session=session)

    async def update_batch(self, entities: List[T], session=None):
        for entity in entities:
            await self._collection.replace_one({"_id": entity.id}, entity.model_dump(), session=session)

    async def get_by_id_aux(self, id: ObjectId) -> Optional[T]:
        doc = await self._collection.find_one({"_id": id})
        return self._model_cls.model_validate(doc) if doc else None

    async def get_by_unique_id_aux(self, unique_id: str) -> Optional[T]:
        doc = await self._collection.find_one({'unique_id': unique_id})
        return self._model_cls.model_validate(doc) if doc else None

    async def get_last_aux(self) -> Optional[T]:
        doc = await self._collection.find_one(sort=[("_id", -1)])
        return self._model_cls.model_validate(doc) if doc else None

    async def get_first_aux(self) -> Optional[T]:
        doc = await self._collection.find_one(sort=[("_id", 1)])
        return self._model_cls.model_validate(doc) if doc else None

    async def exists_record(self, field: str, value: Any) -> bool:
        count = await self._collection.count_documents({field: value})
        return count > 0

    async def exists_excluding_id(self, unique_id: str, filters: dict) -> bool:
        or_conditions = [{k: v} for k, v in filters.items()]
        query = {"unique_id": {"$ne": unique_id}, "$or": or_conditions}
        count = await self._collection.count_documents(query)
        return count > 0
