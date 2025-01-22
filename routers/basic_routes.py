from fastapi import APIRouter, status

router = APIRouter()

@router.get("/health_check", status_code=status.HTTP_200_OK)
def check_health():
    """
    Checks health of server
    Simply returns Ok status
    :return:
    """
    return