from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from core.database import get_db
from model.dto import FrontendJson, QueryMetaData, QueryDTO
from service.db_service import save_query_meta_data
from service.cube import CubeCollection

router = APIRouter()

@router.get("/v1/cube/{cube_name}/front-fields")
async def get_front_fields(cube_name: str, request: Request):
    """
    Query to retrieve info about
    :param request: standard requests
    :param cube_name: Name of the cube
    :return:
    """
    cubes: CubeCollection = request.state.cubes
    return cubes.get_front_fields(cube_name)


@router.get("/v1/cube/{cube_name}/query_info")
def get_query_info(cube_name: str, front_data: FrontendJson, request: Request, db: Session = Depends(get_db)) \
        -> QueryDTO:
    """
    Get query id, number of pages and items per page

    :param request: standard request
    :param db: required db connection
    :param cube_name: Name of the cube
    :param front_data: JSON payload with data, that we want to get from cube
    :return: QueryDTO
    """

    front_data_dict: dict = front_data.model_dump(mode='json')

    cubes: CubeCollection = request.state.cubes

    query_info: QueryMetaData = cubes.get_query_meta(cube_name, front_data)

    qry = save_query_meta_data(db, query_info, front_data_dict)

    query_dto: QueryDTO = QueryDTO(id = qry.id, pages=qry.pages, items_per_page=qry.items_per_page)

    return query_dto


@router.get("/v1/cube/{cube_name}/query_id/{query_id}")
def get_data_by_page(cube_name: str, query_id: int, request: Request, page: int = 0,
                           db: Session = Depends(get_db)):


    cubes: CubeCollection = request.state.cubes

    result: dict = cubes.select_data_by_pages(cube_name, query_id, page, db)

    return result
