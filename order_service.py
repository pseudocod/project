from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db.database import get_db
from db.schema.order import Order
from db.schema.order_item import OrderItem
from db.schema.product import Product
from models.order import OrderItemResponseDTO, OrderRequestDTO, OrderResponseDTO
from utils.exceptions import (
    InsufficientStockException,
    ProductNotActiveException,
    ProductNotFoundException,
)


class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def create_order(
        self, user_id: int, order_request: OrderRequestDTO
    ) -> OrderResponseDTO:
        order_items = []

        for item in order_request.items:
            product = (
                self.db.query(Product)
                .filter(Product.id == item.product_id)
                .with_for_update()
                .first()
            )

            if not product:
                raise ProductNotFoundException(item.product_id)

            if not product.is_active:
                raise ProductNotActiveException(item.product_id)

            if product.stock_quantity < item.quantity:
                raise InsufficientStockException(
                    item.product_id, product.stock_quantity, item.quantity
                )

            product.stock_quantity -= item.quantity

            order_items.append(
                OrderItem(
                    product_id=product.id,
                    name=product.name,
                    quantity=item.quantity,
                    price_per_piece=product.price,
                )
            )

        order = Order(
            user_id=user_id,
            payment_type=order_request.payment_type,
            status="pending",
            shipping_address_id=order_request.shipping_address_id,
            billing_address_id=order_request.billing_address_id,
            updated_by=user_id,
            order_items=order_items,
        )

        try:
            self.db.add(order)
            self.db.commit()
            self.db.refresh(order)
        except SQLAlchemyError:
            self.db.rollback()
            raise

        return OrderResponseDTO(
            id=order.id,
            status=order.status,
            payment_type=order.payment_type,
            shipping_address_id=order.shipping_address_id,
            billing_address_id=order.billing_address_id,
            items=[
                OrderItemResponseDTO(
                    product_id=oi.product_id,
                    name=oi.name,
                    quantity=oi.quantity,
                    price_per_piece=float(oi.price_per_piece),
                )
                for oi in order.order_items
            ],
        )


def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    return OrderService(db)
