import random
import string
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.config import settings
from core.utils.exceptions import UserNotFound
from model.base_model import AppUser, ConfirmationCode, OlapTable
from service.db import get_confirmation_code, create_confirmation_code, get_user_by_username

bcrypt_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/v1/user/authenticate")


def create_jwt(username: str, user_id: int) -> str:
    """
    Creates JWT

    {
        sub: username
        id: user_id
        exp: expiration date
    }

    :param username: Username
    :param user_id: Id
    :return: JWToken with user data
    """
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
        code = generate_random_string(56)
        confirmation_code = get_confirmation_code(code, db)

    current_datetime: datetime = datetime.now()
    expiration_datetime: datetime = current_datetime + timedelta(settings.EXPIRE_CONFIRMATION_CODE)

    new_confirmation_code: ConfirmationCode = ConfirmationCode(code=code, active=True, created_at=current_datetime,
                                                               expires_at=expiration_datetime,
                                                               user=user)

    create_confirmation_code(new_confirmation_code, db)

    return code


def generate_random_string(number_of_symbols: int):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(
        number_of_symbols))


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

def get_user_from_jwt(token: Annotated[str, Depends(oauth2_bearer)]) -> str:
    """
    Get user name from JWToken
    :param token: JWT

    :raises JWTError: if user not found or expired
    :return: username str
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str | None = payload.get("sub")
        user_id: str | None = payload.get("id")
        expiration_date: str | None = payload.get("exp")
        if username is None or user_id is None:
            raise UserNotFound
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не смог проверить JWT",
                            headers={"WWW-Authenticate": "Bearer"},)

    if datetime.fromtimestamp(int(expiration_date)) < datetime.now():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT просрочен",
                            headers={"WWW-Authenticate": "Bearer"}, )

    return username

def cube_security_check(username: str, cube_name: str, db: Session) -> None:
    """
    Checks if user has access to cube

    :param username: username
    :param cube_name: cube_name
    :param db: Session
    :raises HTTPException: if No access to cube
    :return: None
    """
    app_user: AppUser = get_user_by_username(username, db)

    cubes: list[OlapTable] = app_user.olap_tables

    cubes_user_can_access = []

    for cube in cubes:
        cubes_user_can_access.append(cube.name)

    if cube_name not in cubes_user_can_access:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Нет доступа к кубу")
