from comradewolf.utils.enums_and_field_dicts import FilterTypes, WhereConditionType
from pydantic import BaseModel, EmailStr


class SelectFrontendPayload(BaseModel):
    field_name: str


class CalculationFrontendPayload(BaseModel):
    field_name: str
    calculation: str


class WhereFrontendPayload(BaseModel):
    field_name: str
    where: WhereConditionType
    condition: str | list[str]



class FrontendFieldsJson(BaseModel):
    """
    JSON from frontend
    """

    SELECT: list[SelectFrontendPayload]
    CALCULATION: list[CalculationFrontendPayload]
    WHERE: list[WhereFrontendPayload]


class FrontendDistinctStructure(BaseModel):
    """
    FrontendDistinctFields inner structure
    """
    field_name: str
    type: FilterTypes


class FrontendDistinctJson(BaseModel):
    """
    Structure to query to get dimension helper for filters
    """
    SELECT_DISTINCT: FrontendDistinctStructure


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

class UserRegisterDTO(BaseModel):
    """
    User register. Comes from frontend
    """
    username: str
    password: str
    email: EmailStr

class MessageOnly(BaseModel):
    """
    Send any message
    """
    message: str

