from enum import StrEnum


class EventType(StrEnum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    

class OutboxStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"