NO_OLAP_TABLE_IN_COLLECTION_ERROR_NO = 1
NO_CUBE_IN_COLLECTION = 2
NO_QUERY_NUMBER = 3
USER_NOT_FOUND = 4
WRONG_PASSWORD = 5
USER_EXISTS = 6
MAIL_EXISTS = 7
NO_CONFIRMATION_CODE = 8
USER_IS_ACTIVE = 9
CODE_EXPIRED = 10
USER_IS_NOT_ACTIVE = 11
PASSWORD_CODE_EXPIRED = 12
PASSWORD_CODE_EXISTS = 13
NO_FORGOT_PASSWORD_CODE = 14
NO_CUBES_FOR_USER = 15

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

        super().__init__(NO_CUBE_IN_COLLECTION, message)


class NoQuery(ComradeWolfApiException):
    """
    Exception
    """

    def __init__(self, username: str):
        message: str = f"No SQL query"

        super().__init__(NO_QUERY_NUMBER, message)

class UserNotFound(ComradeWolfApiException):
    """
    User not found
    """
    def __init__(self, username: str):
        message: str = f"{username} not found"

        super().__init__(USER_NOT_FOUND, message)


class WrongPassword(ComradeWolfApiException):
    """
    Password did not match
    """
    def __init__(self, username: str):
        message: str = f"{username} password did not match"

        super().__init__(WRONG_PASSWORD, message)

class UserAlreadyExists(ComradeWolfApiException):
    """
    User exists
    """
    def __init__(self, username: str):
        message: str = f"{username} already exists"

        super().__init__(USER_EXISTS, message)

class UserWithMailAlreadyExists(ComradeWolfApiException):
    """
    User with email exists
    """
    def __init__(self, email: str):
        message: str = f"{email} already exists"

        super().__init__(MAIL_EXISTS, message)

class NoConfirmationCode(ComradeWolfApiException):
    """
    Confirmation code was not found
    """
    def __init__(self):
        message: str = f"Confirmation code does not exist"

        super().__init__(NO_CONFIRMATION_CODE, message)



class UserIsActiveAlready(ComradeWolfApiException):
    """
    Confirmation code was not found
    """

    def __init__(self):
        message: str = f"User is already active"

        super().__init__(USER_IS_ACTIVE, message)


class CodeActivationExpired(ComradeWolfApiException):
    """
    Confirmation code was not found
    """

    def __init__(self):
        message: str = f"Code is expired"

        super().__init__(CODE_EXPIRED, message)


class UserIsNotActivated(ComradeWolfApiException):
    """
    Confirmation code was not found
    """

    def __init__(self):
        message: str = f"User is not activated"

        super().__init__(USER_IS_NOT_ACTIVE, message)

class ForgotPasswordCodeExpired(ComradeWolfApiException):
    """
    Password confirmation code was not found
    """

    def __init__(self):
        message: str = f"Password code is expired"

        super().__init__(PASSWORD_CODE_EXPIRED, message)

class ForgotPasswordExists(ComradeWolfApiException):
    """
    Password confirmation code was not found
    """

    def __init__(self):
        message: str = f"Password code exists"

        super().__init__(PASSWORD_CODE_EXISTS, message)

class NoForgotPasswordCode(ComradeWolfApiException):
    """
    Password confirmation code was not found
    """

    def __init__(self):
        message: str = f"Password code does not exist"

        super().__init__(NO_FORGOT_PASSWORD_CODE, message)

class NoCubesForUser(ComradeWolfApiException):
    """
    If user has no cubes assigned to him
    """
    def __init__(self, username: str, user_id: int):
        message: str = f"No Olap Cubes For User #{user_id} {username}"

        super().__init__(NO_CUBES_FOR_USER, message)
