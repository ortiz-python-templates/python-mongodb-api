from typing import Optional, Literal
from fastapi import Query


class SearchFilter:
    def __init__(
        self,
        search_param: Optional[str] = Query(None, alias="search_param"),
        sort_order: Literal["asc", "desc"] = Query("asc", alias="sort_order"),
    ):
        self.search_param = search_param
        self.sort_order = sort_order
