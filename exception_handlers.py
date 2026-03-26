from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .exceptions import (
    InsufficientStockException,
    ProductNotActiveException,
    ProductNotFoundException,
    UserNotFoundException,
    InvalidAttributeFormatException,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ProductNotFoundException)
    def product_not_found_handler(request: Request, exc: ProductNotFoundException):
        return JSONResponse(status_code=404, content={"detail": exc.message})

    @app.exception_handler(UserNotFoundException)
    def user_not_found_handler(request: Request, exc: UserNotFoundException):
        return JSONResponse(status_code=404, content={"detail": exc.message})

    @app.exception_handler(InvalidAttributeFormatException)
    def invalid_attribute_format_handler(
        request: Request, exc: InvalidAttributeFormatException
    ):
        return JSONResponse(status_code=400, content={"detail": exc.message})

    @app.exception_handler(ProductNotActiveException)
    def product_not_active_handler(request: Request, exc: ProductNotActiveException):
        return JSONResponse(status_code=409, content={"detail": exc.message})

    @app.exception_handler(InsufficientStockException)
    def insufficient_stock_handler(request: Request, exc: InsufficientStockException):
        return JSONResponse(status_code=409, content={"detail": exc.message})
