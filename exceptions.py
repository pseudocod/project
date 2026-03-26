class ProductNotFoundException(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        self.message = f"Product with ID {product_id} not found."
        super().__init__(self.message)


class UserNotFoundException(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.message = f"User with ID {user_id} not found"
        super().__init__(self.message)


class InvalidAttributeFormatException(Exception):
    def __init__(self, attr: str):
        self.attr = attr
        self.message = (
            f"Invalid attribute format: '{attr}'. Expected format is 'name:value'."
        )
        super().__init__(self.message)


class MissingTokenException(Exception):
    def __init__(self):
        self.message = "Missing or invalid Authorization header"
        super().__init__(self.message)


class ExpiredTokenException(Exception):
    def __init__(self):
        self.message = "Token has expired"
        super().__init__(self.message)


class InvalidTokenException(Exception):
    def __init__(self):
        self.message = "Invalid token"
        super().__init__(self.message)


class ProductNotActiveException(Exception):
    def __init__(self, product_id: int):
        self.message = f"Product with ID {product_id} is not available."
        super().__init__(self.message)


class InsufficientStockException(Exception):
    def __init__(self, product_id: int, available: int, requested: int):
        self.message = (
            f"Insufficient stock for product {product_id}: "
            f"requested {requested}, available {available}."
        )
        super().__init__(self.message)
