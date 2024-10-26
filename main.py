from fastapi import FastAPI
from .router import olap_router

app = FastAPI()

app.include_router(olap_router.router)
