from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from src.db.database import Base


class ProductAttribute(Base):
    __tablename__ = "product_attribute"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    value = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=now())
    updated_at = Column(DateTime(timezone=True), onupdate=now())

    product_links = relationship(
        "ProductAttributeLink", back_populates="attribute", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            "value = LOWER(value)", name="ck_product_attribute_value_lower"
        ),
    )
