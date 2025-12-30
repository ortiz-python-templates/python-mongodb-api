from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import Field
from bson import ObjectId
from src.common.config.env_config import EnvConfig
from src.core.models.outbox.enums import EventType, OutboxStatus
from src.core.shared.models.base_mongo_model import BaseMongoModel


class OutboxModel(BaseMongoModel):
    # Event data
    payload: Dict[str, Any]

    # Broker routing
    routing_key: str
    exchange: str
    event_type: EventType

    # Entity traceability
    owner_entity: str
    owner_id: ObjectId

    # Delivery state
    status: OutboxStatus = Field(default=OutboxStatus.PENDING)
    
    # Timing
    scheduled_for: datetime = datetime.now(timezone.utc)
    processed_at: Optional[datetime] = None # Filled after successful dispatch

    # Resilience logic
    retry_count: int = 0
    max_retries: int = EnvConfig.OUTBOX_MAX_RETRIES
    last_error: Optional[str] = None # Error details for debugging
    