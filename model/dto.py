from typing import Optional

from pydantic import BaseModel



class SelectFrontendPayload(BaseModel):
    field_name: str


class CalculationFrontendPayload(BaseModel):
    field_name: str
    calculation: str


class WhereFrontendPayload(BaseModel):
    field_name: str
    where: str
    condition: str | list[str]



class FrontendJson(BaseModel):
    """
    JSON from frontend
    """

    SELECT: list[SelectFrontendPayload]
    CALCULATION: list[CalculationFrontendPayload]
    WHERE: list[WhereFrontendPayload]


class QueryMetaData(BaseModel):
    sql_query: str
    rows_no: int
    pages: int
    items_per_page: int
    cube_name: str

class QueryDTO(BaseModel):
    id: int
    pages: int
    items_per_page: int
