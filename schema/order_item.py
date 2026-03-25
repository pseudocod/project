from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, Numeric, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from src.db.database import Base


class OrderItem(Base):
    __tablename__ = "order_item"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, ForeignKey("product.id"), nullable=False, index=True)

    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_piece = Column(Numeric(10, 2), nullable=False)

    order_id = Column(Integer, ForeignKey("order.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=now())
    updated_at = Column(DateTime(timezone=True), onupdate=now())

    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_order_item_quantity_positive"),
        CheckConstraint("price_per_piece > 0", name="ck_order_item_price_positive"),
    )

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
