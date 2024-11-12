import math
import time
from threading import Semaphore

from comradewolf.utils.olap_data_types import SelectCollection
from sqlalchemy import Engine, text, CursorResult

from core.config import Settings
from model.dto import QueryMetaData
from service.optimizer_interface import OptimizerAbstract


class OptimizerPostgres(OptimizerAbstract):
    __connections_semaphore: Semaphore
    __engine: Engine
    __settings: Settings

    def __init__(self, max_connections: int, engine: Engine):
        super().__init__(max_connections, engine)
        self.__connections_semaphore = Semaphore(value=max_connections)
        self.__engine = engine
        self.__settings = Settings()

    def get_query_meta_data(self, cube_name: str, select_collection: SelectCollection) -> QueryMetaData:
        """
        Select best query and check we can return it
        :param cube_name: Name of the qube
        :param select_collection: collection of possible queries
        :return: query_meta_data - query, number of rows and pages
        """
        rows_no: int
        is_ok_to_download_data: bool

        sql_query: str = self.select_best_query(cube_name, select_collection)

        rows_no, is_ok_to_download_data = self.count_rows(sql_query, self.get_max_rows())

        if not is_ok_to_download_data:
            raise RuntimeError

        items_per_page: int = self.get_rows_per_page()
        pages: int = math.ceil(rows_no / items_per_page)

        query_meta_data = QueryMetaData(sql_query=sql_query, rows_no=rows_no, pages=pages,
                                        items_per_page=items_per_page, cube_name=cube_name)

        return query_meta_data


    def select_page_from_olap(self, sql: str, page_no: int, items_per_page: int) -> CursorResult:
        """
        Select one page from olap
        Should use pager with offset and limit
        :param sql: sql query
        :param page_no: page we want to download
        :param items_per_page: how many items per page
        :return: Cursor result from query
        """

        offset: int = page_no * items_per_page

        sql_query = f"{sql} \noffset {offset} limit {items_per_page}"

        engine: Engine = self.get_engine()

        self.__connections_semaphore.acquire()
        print("SEM_START", self.__connections_semaphore)
        try:


            with engine.connect() as connect:
                result = connect.execute(text(sql_query))
        finally:
            i = 5
            while i > 0:
                i = i - 1
                time.sleep(1)
                print(i)
            print("SEM_FINISH", self.__connections_semaphore)
            self.__connections_semaphore.release()

        return result



    def select_best_query(self, cube_name: str, select_collection: SelectCollection) -> str:
        """
        Select best query from SelectCollection
        First query with the list amount of not selected fields

        :param cube_name: name of the cube
        :param select_collection: all possible queries
        :return: select string
        """
        # Unused by OptimizerPostgres
        del cube_name

        query: str = ""
        number_of_fields: int | None = None

        for table in select_collection:
            if (number_of_fields is None) or (number_of_fields > select_collection.get_not_selected_fields_no(table)):
                number_of_fields = select_collection.get_not_selected_fields_no(table)
                query = select_collection.get_sql(table)

        return query


    def count_rows(self, sql: str, max_rows_no: int = 1_000_000) -> tuple[int, bool]:
        """
        Count rows in select. If query returned more rows than :param max_rows_no:, return false. Else true
        :param max_rows_no: Max number of rows that query should return
        :param sql: query
        :return:
                [0] number of rows
                [1] true if number of rows more than max_rows_no
        """

        sql_count = f"select count(*) as count_rows from ({sql}) as q"
        is_ok_to_download_data: bool = False

        rows_no: int
        engine: Engine = self.get_engine()

        self.__connections_semaphore.acquire()

        try:
            with engine.connect() as connect:
                rows_no = connect.execute(text(sql_count)).fetchone()[0]
        finally:
            self.__connections_semaphore.release()

        if rows_no <= max_rows_no:
            is_ok_to_download_data = True

        return rows_no, is_ok_to_download_data
