from sqlalchemy import Boolean, Integer, Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.db.database import Base
from sqlalchemy.sql.functions import now


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=now())
    updated_at = Column(DateTime(timezone=True), onupdate=now())

    products = relationship("Product", back_populates="category")
