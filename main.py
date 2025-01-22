from contextlib import asynccontextmanager

from fastapi import FastAPI

from olap_info.olap_sales_cube import set_cube
from routers import basic_routes

from routers.v1 import olap_router, user_router


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
app.include_router(user_router.router)
app.include_router(basic_routes.router)
