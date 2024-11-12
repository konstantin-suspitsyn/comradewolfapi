"""
File for test cube
"""

from comradewolf.universe.olap_language_select_builders import OlapPostgresSelectBuilder
from comradewolf.universe.olap_prompt_converter_service import OlapPromptConverterService
from comradewolf.universe.olap_service import OlapService
from comradewolf.universe.olap_structure_generator import OlapStructureGenerator
from sqlalchemy import Engine, create_engine
import os
from dotenv import load_dotenv

from service.cube import CubeCollection
from service.optimizer_interface import OptimizerAbstract
from service.optimizer_postgres import OptimizerPostgres

load_dotenv()


def generate_postgres_engine() -> Engine:
    """
    Generates postgres engine
    :return:
    """
    olap_user = os.getenv("OLAP_USER")
    olap_password = os.getenv("OLAP_PASSWORD")
    olap_host = os.getenv("OLAP_HOST")
    olap_port = os.getenv("OLAP_PORT")
    olap_db = os.getenv("OLAP_DB")
    engine: Engine = create_engine(f"postgresql+psycopg2://{olap_user}:{olap_password}@{olap_host}:{olap_port}/"
                                   f"{olap_db}")

    return engine

def generate_postgres_optimizer() -> OptimizerAbstract:
    return OptimizerPostgres(2, generate_postgres_engine())

def comrade_olap_service() -> OlapService:
    olap_select_builder = OlapPostgresSelectBuilder()
    return OlapService(olap_select_builder)

def comrade_olap_structure_generator() -> OlapStructureGenerator:
    osg = OlapStructureGenerator(r"C:\Users\Const\working\comradewolfapi\olap_info\olap_sales")
    return osg

def generate_olap_prompt_converter_service() -> OlapPromptConverterService:
    return OlapPromptConverterService(OlapPostgresSelectBuilder())

def set_cube() -> CubeCollection:
    cc = CubeCollection()
    cc.add_cube("olap_sales", generate_postgres_optimizer(), generate_olap_prompt_converter_service(),
                comrade_olap_structure_generator(), comrade_olap_service())

    return cc
