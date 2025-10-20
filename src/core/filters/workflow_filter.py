from typing import Optional
from fastapi import Query
from src.core.filters.date_range_filter import DateRangeFilter


class WorkflowFilter(DateRangeFilter):
    def __init__(
        self,
        status: Optional[str] = Query(None, alias="status"),
        start_date: Optional[str] = Query(None, alias="start_date"),
        end_date: Optional[str] = Query(None, alias="end_date")
    ):
        super().__init__(start_date=start_date, end_date=end_date)
        self.status = status
