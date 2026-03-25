from sqlalchemy import Boolean, Integer, Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from src.db.database import Base


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    country = Column(String, nullable=False, default="Romania")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=now())
    updated_at = Column(DateTime(timezone=True), onupdate=now())

    user = relationship("User", back_populates="address")
