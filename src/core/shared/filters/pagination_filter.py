from fastapi import Query


class PaginationFilter:
    def __init__(
        self,
        page_index: int = Query(0, alias="page_index", ge=0),
        page_size: int = Query(10, alias="page_size", gt=0),
    ):
        self.page_index = page_index
        self.page_size = page_size