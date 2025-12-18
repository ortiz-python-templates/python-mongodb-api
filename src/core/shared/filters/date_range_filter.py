from typing import Optional
from fastapi import Query


class DateRangeFilter:
    def __init__(
        self,
        status: Optional[str] = Query(None, alias="status"),
        start_date: str = Query(..., alias="start_date"),
        end_date: str = Query(..., alias="end_date"),
    ):
        self.status = status
        self.start_date = start_date
        self.end_date = end_date