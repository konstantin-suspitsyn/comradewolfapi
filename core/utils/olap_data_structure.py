from collections import UserDict

from comradewolf.utils.olap_data_types import OlapTablesCollection, OlapFrontend
from sqlalchemy import Engine

from service.optimizer_interface import OptimizerAbstract
from core.utils.exceptions import NoOlapDataStructureInCollection


class OlapDataStructure(UserDict):
    """
    Class represents all data that you need to build, optimize and query data from database
    """

    def __init__(self, optimizer: OptimizerAbstract, tables_collection: OlapTablesCollection,
                 fields_for_frontend: OlapFrontend) -> None:

        """
        Builds OlapDataStructure
        :param optimizer: implementation of OptimizerAbstract
        :param tables_collection: OlapTablesCollection
        :param fields_for_frontend: OlapFrontend
        """

        structure = {
            "optimizer": optimizer,
            "tables_collection": tables_collection,
            "fields_for_frontend": fields_for_frontend,
        }

        super().__init__(structure)

    def get_optimizer(self) -> OptimizerAbstract:
        """
        Get optimiser for database queries
        :return: OptimizerAbstract implementation
        """
        return self.data["optimizer"]

    def get_tables_collection(self) -> OlapTablesCollection:
        """
        Get olap tables collection
        :return: OlapTablesCollection
        """
        return self.data["tables_collection"]

    def get_fields_for_frontend(self) -> OlapFrontend:
        """
        Get tables for frontend that represent olap table fields
        :return: OlapFrontend
        """
        return self.data["fields_for_frontend"]

    def get_engine(self) -> Engine:
        """
        Get engine from OptimizerAbstract
        :return: Engine
        """
        return self.get_optimizer().get_engine()



class OlapDataStructureCollection(UserDict):
    """
    Dictionary that contains all olap structures available in structure:
    {
        "olap_table_name": OlapDataStructure,
        "olap_table_name": OlapDataStructure,
        ...,
    }
    """
    def add_olap_table(self, olap_table_name: str, olap_data_structure: OlapDataStructure) -> None:
        """
        Adds one olap table structure to collection
        :param olap_table_name: name of table. Same name should be used in queries, databases and so on
        :param olap_data_structure: OlapDataStructure
        :return: None
        """
        self.data[olap_table_name] = olap_data_structure

    def get_olap_data_structure(self, olap_table_name: str) -> OlapDataStructure:
        """
        Get OlapDataStructure by name
        :param olap_table_name: olap table name

        :raises NoOlapDataStructureInCollection: if olap_table_name is not presented

        :return: OlapDataStructure
        """
        if olap_table_name not in self.data:
            raise NoOlapDataStructureInCollection(olap_table_name)

        return self.data[olap_table_name]

    def get_optimizer(self, olap_table_name: str) -> OptimizerAbstract:
        """
        Get optimiser for database queries
        :param olap_table_name: olap table name
        :return: OptimizerAbstract implementation
        """
        return self.get_olap_data_structure(olap_table_name).get_optimizer()

    def get_tables_collection(self, olap_table_name: str) -> OlapTablesCollection:
        """
        Get olap tables collection
        :param olap_table_name: olap table name
        :return: OlapTablesCollection
        """
        return self.get_olap_data_structure(olap_table_name).get_tables_collection()

    def get_fields_for_frontend(self, olap_table_name: str) -> OlapFrontend:
        """
        Get tables for frontend that represent olap table fields
        :param olap_table_name: olap table name
        :return: OlapFrontend
        """
        return self.get_olap_data_structure(olap_table_name).get_fields_for_frontend()

    def get_engine(self, olap_table_name: str) -> Engine:
        """
        Get engine from OptimizerAbstract
        :return: Engine
        """
        return self.get_olap_data_structure(olap_table_name).get_engine()

