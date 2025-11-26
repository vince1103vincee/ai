"""API Client for querying backend API server"""
from .base import BaseClient
from .routes import ProductsMixin, UsersMixin, OrdersMixin, InventoryMixin


class APIClient(BaseClient, ProductsMixin, UsersMixin, OrdersMixin, InventoryMixin):
    """Main API client combining all resource operations

    Methods are organized by resource type in separate modules:
    - Products: get_all_products, get_product, search_products_*
    - Users: get_all_users, get_user, search_users_*, get_user_orders
    - Orders: get_all_orders
    - Inventory: get_inventory, get_product_inventory, get_low_stock_products
    """
    pass
