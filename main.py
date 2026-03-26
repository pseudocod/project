from fastapi import FastAPI

from .utils.settings import settings
from .utils.lifespan import lifespan
from .utils.exception_handlers import register_exception_handlers
from .api.routes import products_router, auth_router, users_router, orders_router
from .api.middlewares.jwt_middleware import JWTMiddleware
from .utils.openapi import configure_openapi

app = FastAPI(lifespan=lifespan)
app.add_middleware(JWTMiddleware)
register_exception_handlers(app)
configure_openapi(app) 

app.include_router(products_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(orders_router)


@app.get("/")
def read_root():
    return {"Hello": f"Leon ({settings.key})"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
