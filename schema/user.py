from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now
from src.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    address_id = Column(Integer, ForeignKey("address.id"), index=True)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False, index=True)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=now())
    updated_at = Column(DateTime(timezone=True), onupdate=now())

    role = relationship("Role", back_populates="users")
    orders = relationship("Order", back_populates="owner")
    cart_entries = relationship(
        "CartEntry", back_populates="user", cascade="all, delete-orphan"
    )
    address = relationship("Address", back_populates="user")
