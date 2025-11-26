"""Route mixins for API client"""
from .products import ProductsMixin
from .users import UsersMixin
from .orders import OrdersMixin
from .inventory import InventoryMixin

__all__ = [
    'ProductsMixin',
    'UsersMixin',
    'OrdersMixin',
    'InventoryMixin',
]
