from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from src.db.database import Base


class ProductAttributeLink(Base):
    __tablename__ = "product_attribute_link"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    attribute_id = Column(Integer, ForeignKey("product_attribute.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=now())

    product = relationship("Product", back_populates="attribute_links")
    attribute = relationship("ProductAttribute", back_populates="product_links")

    __table_args__ = (
        UniqueConstraint("product_id", "attribute_id", name="unique_product_attribute"),
    )