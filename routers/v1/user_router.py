from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.database import get_db
from core.utils.exceptions import UserAlreadyExists, UserWithMailAlreadyExists, NoConfirmationCode, UserIsActiveAlready, \
    CodeActivationExpired
from model.dto import UserRegisterDTO, MessageOnly
from service.user import create_new_user, activate_user_code

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/user/authenticate")

@router.post("/v1/user/register", status_code=status.HTTP_201_CREATED)
def register_user(user_dto: UserRegisterDTO, db: Session = Depends(get_db)) -> MessageOnly:

    middle_activation_link: str = r"v1/user/activate"

    try:
        create_new_user(user_dto, db, middle_activation_link)
    except UserAlreadyExists:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Пользователь с именем {user_dto.username} уже существует")
    except UserWithMailAlreadyExists:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Пользователь с почтой {user_dto.email} уже существует")

    user_was_created: MessageOnly = MessageOnly(message="Пользователь создан. Код активации выслан вам на email")

    return user_was_created

@router.get("/v1/user/activate/{code}", status_code=status.HTTP_202_ACCEPTED)
def activate_user(code: str, db: Session = Depends(get_db)):

    message: MessageOnly = MessageOnly(message="Пользователь активирован")

    try:
        activate_user_code(code, db)
    except NoConfirmationCode:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Код активации отсутствует")
    except UserIsActiveAlready:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Пользователь уже активирован")
    except CodeActivationExpired:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Код просрочен. Вам на почту отправлен новый код")

    return message



# @router.get("/v1/user/forgot_password")
# def forgot_password():
#     pass
#
# @router.get("/v1/user/authenticate")
# def forgot_auth():
#     pass
