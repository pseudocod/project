from fastapi import APIRouter, Depends, Request

from api.services.order_service import OrderService, get_order_service
from models.order import OrderRequestDTO, OrderResponseDTO


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponseDTO, status_code=201)
def place_order(
    request: Request,
    order_request: OrderRequestDTO,
    order_service: OrderService = Depends(get_order_service),
):
    user_id = int(request.state.user_id)
    return order_service.create_order(user_id, order_request)
