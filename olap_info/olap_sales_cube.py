"""
File for test cube
"""
from typing import Type

from comradewolf.universe.olap_language_select_builders import OlapPostgresSelectBuilder
from comradewolf.universe.olap_prompt_converter_service import OlapPromptConverterService
from comradewolf.universe.olap_service import OlapService
from comradewolf.universe.olap_structure_generator import OlapStructureGenerator
from sqlalchemy import Engine, create_engine
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from core.database import get_db
from model.base_model import OlapTable
from service.cube import CubeCollection
from service.db import get_all_olap_cubes
from service.optimizer_factory import OptimizerFactory, SelectBuilderFactory
from service.optimizer_interface import OptimizerAbstract
from service.optimizer_postgres import OptimizerPostgres

load_dotenv()

async def set_cubes() -> CubeCollection:
    cubes_collection = CubeCollection()

    session: Session = await get_db()
    possible_cubes: list[Type[OlapTable]] = get_all_olap_cubes(session)

    for cube in possible_cubes:
        cube_name = cube.name
        toml_link = cube.toml_link
        olap_user = cube.username_env
        olap_password = cube.password_env
        olap_host = cube.host
        olap_port = cube.port
        olap_engine_name = str(cube.engine)
        olap_db = cube.database
        olap_max_connections = cube.max_connections

        engine: Engine = create_engine(f"{olap_engine_name}://{olap_user}:{olap_password}@{olap_host}:{olap_port}/"
                                       f"{olap_db}")

        optimizer: OptimizerAbstract = OptimizerFactory.get(engine_name=olap_engine_name,
                                                            max_connections=int(olap_max_connections),
                                                            engine=engine)

        olap_prompt_converter: OlapPromptConverterService = OlapPromptConverterService(OlapPostgresSelectBuilder())

        osg: OlapStructureGenerator = OlapStructureGenerator(toml_link)

        olap_select_builder = SelectBuilderFactory.get(olap_engine_name)
        olap_service: OlapService = OlapService(olap_select_builder)

        cubes_collection.add_cube(cube_name, optimizer, olap_prompt_converter,
                    osg, olap_service)

    return cubes_collection
