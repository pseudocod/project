from sqlalchemy import CheckConstraint, Integer, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.db.database import Base
from sqlalchemy.sql.functions import now


class CartEntry(Base):
    __tablename__ = "cart_entry"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), server_default=now())
    updated_at = Column(DateTime(timezone=True), onupdate=now())

    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_cart_entry_quantity_positive"),
    )

    user = relationship("User", back_populates="cart_entries")
    product = relationship("Product", back_populates="cart_entries")
