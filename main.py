from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from model.dto import FrontendFieldsJson, QueryMetaData
from olap_info.olap_sales_cube import set_cube
from service.db_service import save_query_meta_data


from routers import olap_router


def return_postgres_opt():
    return set_cube()

structure = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    structure["cube_collection"] = return_postgres_opt()
    yield {"cubes": structure["cube_collection"],}
    structure.clear()


app = FastAPI(lifespan=lifespan)

app.include_router(olap_router.router)


