NO_QUERY_NUMBER = 3
NO_OLAP_TABLE_IN_COLLECTION_ERROR_NO = 1


class ComradeWolfApiException(Exception):
    """
    Base exception for all api exceptions
    """
    def __init__(self, exception_number: int, message: str):
        complete_message = f"Error #{exception_number}. {message}"
        # TODO add log to database
        super().__init__(complete_message)

class NoOlapDataStructureInCollection(ComradeWolfApiException):
    """
    Exception
    """
    def __init__(self, olap_table_name):

        message: str = f"{olap_table_name} was not found in collection"

        super().__init__(NO_OLAP_TABLE_IN_COLLECTION_ERROR_NO, message)

class NoCubeInCollection(ComradeWolfApiException):
    """
    Exception
    """
    def __init__(self, cube_name):

        message: str = f"{cube_name} was not found in collection"

        super().__init__(NO_OLAP_TABLE_IN_COLLECTION_ERROR_NO, message)


class NoQuery(ComradeWolfApiException):
    """
    Exception
    """

    message: str = f"No SQL query"

    super().__init__(NO_QUERY_NUMBER, message)
