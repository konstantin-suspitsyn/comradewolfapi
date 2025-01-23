import json
from typing import Type

from sqlalchemy.orm import Session

from core.utils.exceptions import UserAlreadyExists, UserWithMailAlreadyExists, NoConfirmationCode, UserNotFound, \
    NoForgotPasswordCode, NoCubesForUser
from model.base_model import SavedQuery, AppUser, ConfirmationCode, ForgotPasswordCode, OlapTable, user_olap_table
from model.dto import QueryMetaData


def save_query_meta_data(db: Session, query_info: QueryMetaData, frontend: dict) -> SavedQuery:
    saved_query = SavedQuery(frontend = json.dumps(frontend), query = query_info.sql_query, pages=query_info.pages,
                             items_per_page=query_info.items_per_page)
    db.add(saved_query)
    db.commit()
    db.refresh(saved_query)

    return saved_query

def create_user(db: Session, app_user: AppUser) -> AppUser:
    """
    Saves user to DB and returns updated data
    :param db:
    :param app_user: AppUser without id. Id will be created after save

    :raises UserAlreadyExists:
    :raises UserWithMailAlreadyExists:

    :return: updated AppUser
    """

    user_in_db: AppUser | None

    user_in_db = db.query(AppUser).filter(AppUser.username == app_user.username).first()

    if user_in_db is not None:
        raise UserAlreadyExists(app_user.username)

    user_in_db = db.query(AppUser).filter(AppUser.email == app_user.email).first()

    if user_in_db is not None:
        raise UserWithMailAlreadyExists(app_user.email)

    db.add(app_user)
    db.commit()
    db.refresh(app_user)

    return app_user

def get_confirmation_code(code: str, db: Session, is_active: bool | None = True) -> ConfirmationCode | None:
    """
    Get confirmation code if it exists
    :param is_active: code was not activated
    :param db:
    :param code: confirmation code
    :return:
    """
    if is_active is None:
        return db.query(ConfirmationCode).filter(ConfirmationCode.code == code).first()

    return db.query(ConfirmationCode).filter(ConfirmationCode.code == code,
                                             ConfirmationCode.active == is_active).first()



def deactivate_code_for_user(code: str, db: Session) -> AppUser:
    """
    Deactivates confirmation code
    :param code: code string
    :param db: Session
    :return: AppUser bounded to ConfirmationCode
    """
    confirmation_code: ConfirmationCode | None = get_confirmation_code(code, db)

    if confirmation_code is None:
        raise NoConfirmationCode

    confirmation_code.active = False
    app_user: AppUser = confirmation_code.user
    db.flush()
    db.commit()

    return app_user


def create_confirmation_code(new_confirmation_code: ConfirmationCode, db: Session) -> ConfirmationCode:
    """
    Creates ConfirmationCode in database
    :param new_confirmation_code: ConfirmationCode to save, no id, not from database
    :param db:
    :return:
    """
    db.add(new_confirmation_code)
    db.commit()
    db.refresh(new_confirmation_code)

    return new_confirmation_code

def set_user_active(app_user: AppUser, db: Session):
    """
    Change user state to active
    :param app_user: AppUser that needs to be changed
    :param db:
    :return:
    """
    current_app_user: AppUser | None = db.query(AppUser).filter(AppUser.id == app_user.id).first()

    if current_app_user is None:
        raise UserNotFound

    current_app_user.is_active = True

    db.flush()
    db.commit()

def get_user_by_username(username: str, db: Session) -> AppUser | None:
    app_user: AppUser | None = db.query(AppUser).filter(AppUser.username == username).first()
    return app_user

def get_forgot_password_code_by_username(username: str, db: Session) -> ForgotPasswordCode | None:
    app_user: AppUser | None = get_user_by_username(username, db)

    if app_user is None:
        raise UserNotFound

    forgot_password_code: ForgotPasswordCode | None = db.query(ForgotPasswordCode).filter(
        ForgotPasswordCode.user_id == app_user.id, ForgotPasswordCode.is_active == True).first()

    return forgot_password_code

def get_forgot_password_code_by_code(code: str, db: Session) -> ForgotPasswordCode | None:
    forgot_password_code: ForgotPasswordCode | None = db.query(ForgotPasswordCode).filter(
        ForgotPasswordCode.code == code).first()

    return forgot_password_code

def create_forgot_password_code(forgot_password_code: ForgotPasswordCode, db: Session) -> ForgotPasswordCode:
    db.add(forgot_password_code)
    db.commit()
    db.refresh(forgot_password_code)

    return forgot_password_code

def deactivate_password_code(code: str, db: Session) -> None:
    forgot_password_code: ForgotPasswordCode | None = get_forgot_password_code_by_code(code, db)
    if forgot_password_code is None:
        raise NoForgotPasswordCode

    forgot_password_code.is_active = False

    db.flush()
    db.commit()


def get_user_by_id(user_id: int, db: Session):
    app_user: AppUser | None = db.query(AppUser).filter(AppUser.id == user_id).first()

    return app_user

def get_olap_tables_by_user(user: AppUser, db:Session) -> list[Type[OlapTable]]:
    """

    :param user:
    :param db:
    :return:
    """

    olap_tables = db.query(OlapTable).filter(OlapTable.app_users.any(OlapTable.app_users.contains(user))).all()

    if len(olap_tables) == 0:
        raise NoCubesForUser(user.username, user.id)

    return olap_tables

def change_password_for_user_with_id(user_id: int, password: str, db: Session):
    app_user: AppUser = get_user_by_id(user_id, db)

    app_user.password = password

    db.flush()
    db.commit()

def deactivate_forgotten_password_code(forgot_password_code: ForgotPasswordCode, db: Session):
    forgot_password_code.is_active = False
    db.flush()
    db.commit()

def get_all_olap_cubes(db: Session) -> list[Type[OlapTable]]:
    cubes = db.query(OlapTable).all()
    return cubes
