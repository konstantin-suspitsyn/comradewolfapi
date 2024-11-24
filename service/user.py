import random
import string
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.config import settings
from core.utils.exceptions import UserNotFound, WrongPassword, NoConfirmationCode, UserIsActiveAlready, \
    CodeActivationExpired, UserIsNotActivated
from model.base_model import AppUser, ConfirmationCode
from model.dto import UserRegisterDTO
from service.db import create_user, get_confirmation_code, create_confirmation_code, deactivate_code_for_user, \
    set_user_active
from service.mail import send_confirmation_mail

bcrypt_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Gets raw password and creates hash out of it
    :param password: password string
    :return: hashed password
    """
    return bcrypt_context.hash(password)

def check_password(hashed_password: str, raw_password: str) -> bool:
    """
    Compare hashed password and password. If passwords match return True, else return False
    :param hashed_password: hashed password from database
    :param raw_password: raw password from user
    :return: True or False
    """
    return bcrypt_context.verify(raw_password, hashed_password)

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


def authenticate_user(username: str, password: str, db: Session) -> str:
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

    if not check_password(password, app_user.password):
        raise WrongPassword(username)

    return create_jwt(app_user.username, app_user.id)

def create_jwt(username: str, user_id: int) -> str:
    expires = datetime.now() + timedelta(seconds=settings.EXPIRE_JWT_IN)
    encode = {"sub": username, "id": user_id, "exp": expires}
    return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def generate_confirmation_code(user: AppUser, db: Session) -> str:
    """
    Generates confirmation code
    :param user:
    :param db:
    :return:
    """

    code: str = ""
    confirmation_code: ConfirmationCode | None = ConfirmationCode()

    while confirmation_code is not None:
        code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(256))
        confirmation_code = get_confirmation_code(code, db)

    current_datetime: datetime = datetime.now()
    expiration_datetime: datetime = current_datetime + timedelta(settings.EXPIRE_CONFIRMATION_CODE)

    new_confirmation_code: ConfirmationCode = ConfirmationCode(code=code, active=True, created_at=current_datetime,
                                                               expires_at=expiration_datetime,
                                                               user=user)

    create_confirmation_code(new_confirmation_code, db)

    return code

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