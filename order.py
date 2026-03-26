from typing import Literal
from pydantic import BaseModel, Field, model_validator


class OrderItemRequestDTO(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class OrderRequestDTO(BaseModel):
    items: list[OrderItemRequestDTO] = Field(min_length=1)
    payment_type: Literal["cash", "card"]
    shipping_address_id: int = Field(gt=0)
    billing_address_id: int = Field(gt=0)

    @model_validator(mode="after")
    def no_duplicate_products(self):
        product_ids = [item.product_id for item in self.items]
        if len(product_ids) != len(set(product_ids)):
            raise ValueError("Duplicate product IDs are not allowed in the same order.")
        return self


class OrderItemResponseDTO(BaseModel):
    product_id: int
    name: str
    quantity: int
    price_per_piece: float


class OrderResponseDTO(BaseModel):
    id: int
    status: str
    payment_type: str
    shipping_address_id: int
    billing_address_id: int
    items: list[OrderItemResponseDTO]