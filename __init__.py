from .products import router as products_router
from .auth import router as auth_router
from .users import router as users_router
from .orders import router as orders_router

__all__ = ["products_router", "auth_router", "users_router", "orders_router"]
