from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request

from core.database import get_db
from core.utils.exceptions import NoCubesForUser
from model.base_model import SavedQuery
from model.dto import FrontendFieldsJson, QueryMetaData, QueryDTO, FrontendDistinctJson, AvailableCubes
from service.db import save_query_meta_data
from service.cube import CubeCollection
from service.security import get_user_from_jwt, cube_security_check
from service.user import get_available_cubes_for_user

router = APIRouter()

@router.get("/v1/cube/{cube_name}/front-fields")
def get_front_fields(cube_name: str, request: Request, username: str = Depends(get_user_from_jwt),
                     db: Session = Depends(get_db)):
    """
    Query to retrieve info about
    :param db:
    :param username:
    :param request: standard requests
    :param cube_name: Name of the cube
    :return:
    """
    cube_security_check(username, cube_name, db)

    cubes: CubeCollection = request.state.cubes

    return cubes.get_front_fields_dto(cube_name)


@router.post("/v1/cube/{cube_name}/query_info")
def get_query_info(cube_name: str, front_data: FrontendFieldsJson, request: Request, db: Session = Depends(get_db),
                   username: str = Depends(get_user_from_jwt)) -> QueryDTO:
    """
    Get query id, number of pages and items per page

    :param username: username from JWT will be used for auth and cube access confirmation
    :param request: standard request
    :param db: required db connection
    :param cube_name: Name of the cube
    :param front_data: JSON payload with data, that we want to get from cube
    :return: QueryDTO
    """

    cube_security_check(username, cube_name, db)

    # We want to get data using limit-offset
    add_order_by: bool = True

    front_data_dict: dict = front_data.model_dump(mode='json')

    cubes: CubeCollection = request.state.cubes

    query_info: QueryMetaData = cubes.get_query_meta(cube_name, front_data, add_order_by)

    qry: SavedQuery = save_query_meta_data(db, query_info, front_data_dict)

    query_dto: QueryDTO = QueryDTO(id = qry.id, pages=qry.pages, items_per_page=qry.items_per_page)

    return query_dto


@router.get("/v1/cube/{cube_name}/query_id/{query_id}")
def get_data_by_page(cube_name: str, query_id: int, request: Request, page: int = 0,
                     username: str = Depends(get_user_from_jwt), db: Session = Depends(get_db)):
    """
    Gets data from OLAP database by previously saved query in QueryMetaData

    :param username:
    :param cube_name: Name of the cube
    :param query_id: query id of SavedQuery
    :param request: starlette Request. No need to be provided
    :param page: page no to be downloaded query works as offset-limit kind
    :param db: dependency injected Session
    :return: converted to dict data from database
    """

    cube_security_check(username, cube_name, db)

    cubes: CubeCollection = request.state.cubes

    result = cubes.select_data_by_pages(cube_name, query_id, page, db)

    return result

@router.get("/v1/cube/{cube_name}/dimension")
def get_dimension(cube_name: str, dimension_field: FrontendDistinctJson, request: Request,
                  username: str = Depends(get_user_from_jwt), db: Session = Depends(get_db)):
    """
    Gets data from OLAP database with data of current dimension. To help frontend users use filters

    :param db:
    :param username:
    :param dimension_field:
    :param cube_name: Name of the cube
    :param request: starlette Request. No need to be provided
    :return: converted JSON data from database
    """

    cube_security_check(username, cube_name, db)

    cubes: CubeCollection = request.state.cubes

    result = cubes.select_dimension(cube_name, dimension_field)

    return result

@router.get("/v1/cube/available")
def get_available_cubes(username: str = Depends(get_user_from_jwt), db: Session = Depends(get_db)):
    """
    Lists all available cubes
    :param username:
    :param db:
    :return:
    """
    try:
        cubes: AvailableCubes = get_available_cubes_for_user(username, db)
    except NoCubesForUser:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Доступных кубов нет")

    return cubes
