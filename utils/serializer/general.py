from pydantic import BaseModel, validator

class SearchStandardQueryString(BaseModel):

    max_items: int = 50

    @validator("max_items")
    def check_if_max_items_is_valid(cls,v):

        if v <= 100:
            return v

        raise ValueError("Pagination max itens per page must be minor or equal to 100")