import json

from sqlalchemy.orm import Session

from core.utils.exceptions import UserAlreadyExists, UserWithMailAlreadyExists, NoConfirmationCode, UserNotFound
from model.base_model import SavedQuery, AppUser, ConfirmationCode
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
    current_app_user: AppUser | None = db.query(AppUser).filter(AppUser.id == app_user.id).first()

    if current_app_user is None:
        raise UserNotFound

    current_app_user.is_active = True

    db.flush()
    db.commit()
