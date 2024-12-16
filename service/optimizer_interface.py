from abc import ABC, abstractmethod
from threading import Semaphore

from comradewolf.utils.olap_data_types import SelectCollection, SelectFilter
from sqlalchemy import Engine, CursorResult, Sequence

from core.config import Settings
from model.dto import QueryMetaData


class OptimizerAbstract(ABC):

    __connections_semaphore: Semaphore
    __engine: Engine
    __settings: Settings

    def __init__(self, max_connections: int, engine: Engine) -> None:
        """
        Creates optimizer with maximum parallel connections to database
        :param max_connections:
        :param engine:
        """

        self.__connections_semaphore = Semaphore(value=max_connections)
        self.__engine = engine
        self.__settings = Settings()

    def get_max_rows(self) -> int:
        """
        Returns max row number
        :return:
        """
        return self.__settings.QUERY_ROW_LIMIT

    def get_rows_per_page(self) -> int:
        """
        Returns settings per page
        :return:
        """
        return self.__settings.ROWS_PER_PAGE


    def __get_connections_semaphore_value(self):
        print(self.__connections_semaphore.__repr__())
        return self.__connections_semaphore.__repr__()

    def get_engine(self) -> Engine:
        """
        Returns sqlalchemy.Engine
        :return:
        """
        return self.__engine

    @abstractmethod
    def count_rows(self, sql: str, max_rows_no: int = 1_000_000) -> tuple[int, bool]:
        """
        Count rows in select. If query returned more rows than :param max_rows_no:, return false. Else true
        :param max_rows_no: Max number of rows that query should return
        :param sql: query
        :return:
                [0] number of rows
                [1] true if number of rows more than max_rows_no
        """
        pass

    @abstractmethod
    def get_query_meta_data(self, cube_name: str, select_collection: SelectCollection) -> QueryMetaData:
        """
        Get all metadata for a query
        :param cube_name: name of the cube
        :param select_collection: all possible queries
        :return: QueryMetaData
        """
        pass

    @abstractmethod
    def select_best_query(self, cube_name: str, select_collection: SelectCollection) -> str:
        """
        Select best query from SelectCollection
        :param cube_name: name of the cube
        :param select_collection: all possible queries
        :return: select string
        """
        pass

    @abstractmethod
    def select_page_from_olap(self, sql: str, page_no: int, items_per_page: int) -> CursorResult:
        """
        Select one page from olap
        Should use pager with offset and limit
        :param sql: sql query
        :param page_no: page we want to download
        :param items_per_page: how many items per page
        :return: Cursor result from query
        """

    @abstractmethod
    def select_dimension(self, select_filter: SelectFilter) -> CursorResult:
        """
        Selects data from db with unique values for dimension
        :param select_filter: SelectFilter from frontend
        :return:
        """
        pass

    @abstractmethod
    def select_best_filter_query(self, select_filter: SelectFilter) -> str:
        """
        Choose best filter query
        :param select_filter: SelectFilter from frontend
        :return: best select as str
        """
        pass
