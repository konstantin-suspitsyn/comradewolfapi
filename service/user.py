from datetime import datetime, timedelta
from typing import Type

from setuptools.extern import names
from sqlalchemy.orm import Session

from core.config import settings
from core.utils.exceptions import UserNotFound, WrongPassword, NoConfirmationCode, UserIsActiveAlready, \
    CodeActivationExpired, UserIsNotActivated, ForgotPasswordExists, NoForgotPasswordCode
from model.base_model import AppUser, ConfirmationCode, ForgotPasswordCode, OlapTable
from model.dto import UserRegisterDTO, ChangeForgottenPassword, AvailableCubes, OlapCube
from service.db import create_user, get_confirmation_code, deactivate_code_for_user, set_user_active, \
    get_user_by_username, get_forgot_password_code_by_username, create_forgot_password_code, deactivate_password_code, \
    get_forgot_password_code_by_code, get_user_by_id, change_password_for_user_with_id, \
    deactivate_forgotten_password_code, get_olap_tables_by_user
from service.mail import send_confirmation_mail, send_forgot_password_mail
from service.security import create_jwt, hash_password, generate_confirmation_code, check_password, \
    generate_random_string


def create_new_user(user_dto: UserRegisterDTO, db: Session, middle_link: str):
    """
    Creates new user in database
    :param user_dto:
    :param middle_link:
    :param db:
    :return:
    """

    username: str = user_dto.username
    password: str = user_dto.password
    email: str = user_dto.email

    hashed_password: str = hash_password(password)
    app_user: AppUser = AppUser(username=username, password=hashed_password, email=email, created_at=datetime.now())
    app_user = create_user(db, app_user)

    code: str = generate_confirmation_code(app_user, db)

    send_confirmation_mail(code, app_user.email, middle_link)


def authenticate_user_and_return_jwt(username: str, password: str, db: Session) -> str:
    """
    Authenticates user

    :raises UserNotFound: if user was not found in database
    :raises WrongPassword: if passwords did not match
    :raises UserIsNotActivated: if user was not activated

    :param username:
    :param password:
    :param db: Session
    :return: jwt token
    """
    app_user: AppUser | None = db.query(AppUser).filter(AppUser.username == username).first()

    if app_user is None:
        raise UserNotFound(username)

    if not app_user.is_active:
        raise UserIsNotActivated

    if not check_password(app_user.password, password):
        raise WrongPassword(username)

    return create_jwt(app_user.username, app_user.id)



def activate_user_code(code: str, db: Session):
    """
    Activates user code and triggers AppUserActivation
    :param code:
    :param db:
    :return:
    """
    # Check if active code exists
    confirmation_code: ConfirmationCode | None = get_confirmation_code(code, db, None)
    # If no code raise an error
    if confirmation_code is None:
        raise NoConfirmationCode

    app_user: AppUser = confirmation_code.user

    # User is active already
    if app_user.is_active:
        raise UserIsActiveAlready

    if confirmation_code.active:
        deactivate_code_for_user(code, db)

    # Code is expired
    if confirmation_code.expires_at < datetime.now():
        generate_confirmation_code(app_user, db)
        raise CodeActivationExpired

    set_user_active(app_user, db)

def send_forgot_password_code(username: str, db: Session) -> None:
    """

    :param username:
    :param db:
    :raises ForgotPasswordExists:
    :return:
    """
    app_user: AppUser = get_user_by_username(username, db)

    # Check if code exists already
    # If it exists throw an error
    existing_code: ForgotPasswordCode | None = get_forgot_password_code_by_username(username, db)

    if existing_code is not None:
        if existing_code.expires_at < datetime.now():
            # Deactivate code
            deactivate_password_code(existing_code.code, db)
        else:
            raise ForgotPasswordExists

    code: str = generate_random_string(50)

    forgot_password_code: ForgotPasswordCode = ForgotPasswordCode(
        user_id = app_user.id,
        code = code,
        created_at = datetime.now(),
        updated_at = datetime.now(),
        expires_at = datetime.now() + timedelta(seconds=settings.EXPIRE_PASSWORD_RESTORATION_CODE),
        is_active = True
    )

    create_forgot_password_code(forgot_password_code, db)

    send_forgot_password_mail(code, app_user.email)


def change_password_with_code(change_password_dto: ChangeForgottenPassword, db: Session):
    """
    Change Forgotten password
    :param change_password_dto:
    :param db:
    :raises UserNotFound:
    :raises NoForgotPasswordCode:
    :return:
    """

    hashed_password: str

    forgot_password_code: ForgotPasswordCode = get_forgot_password_code_by_code(change_password_dto.forgot_code_token,
                                                                                db)

    if forgot_password_code is None:
        raise NoForgotPasswordCode

    app_user: AppUser | None = get_user_by_id(forgot_password_code.user_id, db)

    if app_user is None:
        raise UserNotFound

    hashed_password = hash_password(change_password_dto.password)

    change_password_for_user_with_id(app_user.id, hashed_password, db)
    deactivate_forgotten_password_code(forgot_password_code, db)

def get_available_cubes_for_user(username:str, db: Session) -> AvailableCubes:
    """
    Get all available cubes
    :param username:
    :param db:
    :return:
    """
    app_user: AppUser = get_user_by_username(username, db)
    olap_tables: list[Type[OlapTable]] = get_olap_tables_by_user(app_user, db)

    available_cubes: AvailableCubes = AvailableCubes(cubes=[])

    for olap_table in olap_tables:
        available_cubes.cubes.append(OlapCube(id=olap_table.id, name=olap_table.name))

    return available_cubes
