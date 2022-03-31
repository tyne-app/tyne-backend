from fastapi import status, APIRouter
from src.dto.response.SimpleResponse import SimpleResponse

health_controller = APIRouter(
    prefix="/health"
)


@health_controller.get('/', status_code=status.HTTP_200_OK)
async def get_client_reservations():
    return SimpleResponse("This app is healthy")
