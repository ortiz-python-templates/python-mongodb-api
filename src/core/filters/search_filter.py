from typing import Optional
from fastapi import Query

class SearchFilter:
    
    def __init__(
        self,
        search_param: Optional[str] = Query(None, alias="search_param")
    ):
        self.search_param = search_param