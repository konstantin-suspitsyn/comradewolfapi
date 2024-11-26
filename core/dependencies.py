from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from main import structure
from model.base_model import AppUser
from service.security import get_user_from_jwt


async def get_cube_info():
    return structure["cube_collection"]

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[str, Depends(get_user_from_jwt)]