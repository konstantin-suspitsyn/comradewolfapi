from collections import UserDict

from comradewolf.universe.olap_prompt_converter_service import OlapPromptConverterService
from comradewolf.universe.olap_service import OlapService
from comradewolf.universe.olap_structure_generator import OlapStructureGenerator
from comradewolf.utils.olap_data_types import OlapFrontend, SelectCollection, OlapFrontendToBackend, OlapFilterFrontend, \
    OlapTablesCollection, SelectFilter
from docutils.nodes import field
from sqlalchemy import Sequence, RowMapping, CursorResult
from sqlalchemy.orm import Session

from core.utils.exceptions import NoCubeInCollection
from model.base_model import SavedQuery
from model.dto import FrontendFieldsJson, QueryMetaData, FrontendDistinctJson, FrontFieldsDTO, FrontFieldProperty
from service.optimizer_interface import OptimizerAbstract


class CubeCollection(UserDict):
    """
    Structure contains all data that will be used for cubes
    """

    def add_cube(self,
                 cube_name:str,
                 optimizer: OptimizerAbstract,
                 prompt_converter_service: OlapPromptConverterService,
                 olap_structure: OlapStructureGenerator,
                 olap_service: OlapService) -> None:
        """
        Adds one cube to collection
        :param cube_name: Name of the cube
        :param optimizer: Optimizer made for correct database type
        :param prompt_converter_service: Converter that correctly converts frontend data to backend-specific data
        :param olap_structure: Complete structure that created from .toml files, that describe cube
        :param olap_service: olap service that creates correct selects from
        :return:
        """
        self.data[cube_name] = {
            "optimizer": optimizer,
            "prompt_converter_service": prompt_converter_service,
            "olap_structure": olap_structure,
            "olap_frontend_fields": olap_structure.get_front_fields(),
            "olap_service": olap_service,
        }

    def get_front_fields(self, cube_name: str) -> OlapFrontend:
        """
        Return front fields DTO of cube
        :param cube_name: name of the cube

        :raises NoCubeInCollection: if  :param cube_name: was not found in collection

        :return: Frontend fields with types and names
        """

        self.__is_cube_in_collection(cube_name)

        olap_frontend: OlapFrontend = self.data[cube_name]["olap_frontend_fields"]

        return olap_frontend

    def get_front_fields_dto(self, cube_name: str) -> FrontFieldsDTO:
        """
        Return front fields DTO of cube
        :param cube_name: name of the cube

        :raises NoCubeInCollection: if  :param cube_name: was not found in collection

        :return: Frontend fields with types and names
        """

        self.__is_cube_in_collection(cube_name)

        olap_frontend: OlapFrontend = self.get_front_fields(cube_name)

        front_fields_dto: FrontFieldsDTO = FrontFieldsDTO(fields=[])

        for field_name_alias in olap_frontend:
            front_fields_dto.fields.append(FrontFieldProperty(
                field_name=field_name_alias,
                field_type=olap_frontend.get_field_type(field_name_alias),
                front_name=olap_frontend.get_front_name(field_name_alias),
                data_type=olap_frontend.get_data_type(field_name_alias),
            ))

        return front_fields_dto

    def get_olap_structure(self, cube_name: str) -> OlapStructureGenerator:
        """
        Return OlapStructureGenerator for cube
        :param cube_name: name of the cube

        :raises NoCubeInCollection: if  :param cube_name: was not found in collection

        :return: OlapStructureGenerator for cube
        """
        self.__is_cube_in_collection(cube_name)

        return self.data[cube_name]["olap_structure"]

    def __is_cube_in_collection(self, cube_name) -> None:
        """
        Checks if cube in collection
        If cube is in collection, it does nothing

        :raises NoCubeInCollection: if cube is not in collection

        :param cube_name: name of the cube
        :return: None
        """
        if cube_name not in self.data:
            raise NoCubeInCollection(cube_name)

    def get_prompt_converter_service(self, cube_name: str) -> OlapPromptConverterService:
        """
        Get OlapPromptConverterService service for cube

        :raises NoCubeInCollection: if  :param cube_name: was not found in collection
        :param cube_name: name of the cube
        :return: OlapPromptConverterService for the cube
        """

        self.__is_cube_in_collection(cube_name)

        return self.data[cube_name]["prompt_converter_service"]

    def get_optimizer(self, cube_name: str) -> OptimizerAbstract:
        """
        Get OptimizerAbstract service for cube

        :raises NoCubeInCollection: if  :param cube_name: was not found in collection
        :param cube_name: name of the cube
        :return: OptimizerAbstract for the cube
        """

        self.__is_cube_in_collection(cube_name)

        return self.data[cube_name]["optimizer"]

    def get_olap_service(self, cube_name: str) -> OlapService:
        """
        Get OlapService  for cube
        :param cube_name: name of the cube

        :raises NoCubeInCollection: if  :param cube_name: was not found in collection

        :return: OlapService for cube
        """

        self.__is_cube_in_collection(cube_name)

        return self.data[cube_name]["olap_service"]

    def get_query_meta(self, cube_name: str, front_data: FrontendFieldsJson, add_order_by: bool) -> QueryMetaData:
        """
        Chooses select statement through optimizer
        Writes select statement to database to select later
        :param add_order_by: Add order by to query or not
            Add it if you want to download data using offset-limit
        :param cube_name: name of the cube
        :param front_data: dictionary with fields and conditions that user demands
        :return: QueryMetaData with query number, number of pages, number of rows per page and total number of rows
        """

        frontend_dict: dict = front_data.model_dump(mode='json')

        optimizer: OptimizerAbstract = self.get_optimizer(cube_name)

        select_collection: SelectCollection = self.get_all_queries(cube_name, frontend_dict, add_order_by)
        query_meta_data: QueryMetaData = optimizer.get_query_meta_data(cube_name, select_collection)

        return query_meta_data

    def get_all_queries(self, cube_name: str, front_data: dict, add_order_by: bool) -> SelectCollection:
        """
        Gets all possible queries from the cube with front_data user needs

        :param cube_name: name of the cube
        :param front_data: dictionary with fields and conditions that user demands
        :param add_order_by: Add order by to query or not
            You should add it if you plan download data by pages

        :raises NoCubeInCollection: if  :param cube_name: was not found in collection

        :return: SelectCollection
        """
        prompt_service: OlapPromptConverterService = self.get_prompt_converter_service(cube_name)
        olap_frontend_fields: OlapFrontend = self.get_front_fields(cube_name)
        olap_service: OlapService = self.get_olap_service(cube_name)
        olap_structure: OlapStructureGenerator = self.get_olap_structure(cube_name)

        frontend_to_backend_type: OlapFrontendToBackend = prompt_service\
            .create_frontend_to_backend(front_data, olap_frontend_fields)

        return olap_service.select_data(frontend_to_backend_type, olap_structure.get_tables_collection(), add_order_by)

    def select_data_by_pages(self, cube_name: str, query_id: int, page: int, db: Session) -> Sequence[RowMapping]:
        """
        Gets data from OLAP database by previously saved query in QueryMetaData

        :param cube_name: name of the cube
        :param query_id: query id of SavedQuery
        :param page: page no to be downloaded query works as offset-limit kind
        :param db: db Session
        :return:
        """

        # Get query to retrieve data from DB
        sql: str
        items_per_page: int

        saved_query: SavedQuery = db.query(SavedQuery).filter(SavedQuery.id == query_id).first()

        sql = saved_query.query
        items_per_page = saved_query.items_per_page

        # Retrieve data
        data_from_db = self.get_optimizer(cube_name=cube_name).select_page_from_olap(
            sql=sql, page_no=page, items_per_page=items_per_page)

        # Convert to smth similar to dict
        dict_from_db: Sequence[RowMapping] = data_from_db.mappings().all()

        return dict_from_db

    def select_dimension(self, cube_name: str, dimension_field: FrontendDistinctJson) -> Sequence[RowMapping]:
        """
        Selects data for one dimension that should be used as
        :param cube_name:
        :param dimension_field:
        :return:
        """
        front_data_dict: dict = dimension_field.model_dump(mode='json')
        front_to_back = OlapFilterFrontend(front_data_dict)

        olap_service: OlapService = self.get_olap_service(cube_name)
        tables_collection: OlapTablesCollection = self.get_olap_structure(cube_name).get_tables_collection()

        select_filter: SelectFilter = olap_service.select_filter_for_frontend(front_to_back, tables_collection)

        optimizer: OptimizerAbstract = self.get_optimizer(cube_name)

        dimension_from_db: CursorResult = optimizer.select_dimension(select_filter)

        return dimension_from_db.mappings().all()
