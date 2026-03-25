from sqlalchemy import Column, ForeignKey, Integer, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from src.db.database import Base


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    payment_type = Column(Enum("cash", "card", name="payment_type"), nullable=False)
    status = Column(
        Enum(
            "pending",
            "confirmed",
            "in_delivery",
            "delivered",
            "completed",
            "cancelled",
            "returned",
            name="order_status",
        ),
        default="pending",
        nullable=False,
    )

    shipping_address_id = Column(Integer, ForeignKey("address.id"), index=True)
    billing_address_id = Column(Integer, ForeignKey("address.id"), index=True)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=now())
    updated_at = Column(DateTime(timezone=True), onupdate=now())

    owner = relationship("User", foreign_keys=[user_id], back_populates="orders")
    order_items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )

    shipping_address = relationship("Address", foreign_keys="Order.shipping_address_id")
    billing_address = relationship("Address", foreign_keys="Order.billing_address_id")
