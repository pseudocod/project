from sqlalchemy import Boolean, CheckConstraint, Integer, Column, Numeric, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from src.db.database import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False, index=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=now())
    updated_at = Column(DateTime(timezone=True), onupdate=now())

    __table_args__ = (
        CheckConstraint("price > 0", name="ck_product_price_positive"),
        CheckConstraint("stock_quantity >= 0", name="ck_product_stock_non_negative"),
    )

    images = relationship(
        "ProductImage", back_populates="product", cascade="all, delete-orphan"
    )
    attribute_links = relationship(
        "ProductAttributeLink", back_populates="product", cascade="all, delete-orphan"
    )
    category = relationship("Category", back_populates="products")
    cart_entries = relationship(
        "CartEntry", back_populates="product", cascade="all, delete-orphan"
    )
    order_items = relationship("OrderItem", back_populates="product")
