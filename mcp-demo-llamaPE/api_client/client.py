"""API Client for querying the Flask API Server"""
import requests
from typing import Any, Dict, List, Optional
from config.settings import API_SERVER_URL, API_SERVER_TIMEOUT


class APIClient:
    """Client for interacting with the Flask API Server"""

    def __init__(self, base_url: str = API_SERVER_URL, timeout: int = API_SERVER_TIMEOUT):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to API server"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.request(
                method,
                url,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """GET request"""
        return self._request('GET', endpoint, params=params)

    def health_check(self) -> Dict[str, Any]:
        """Check API server health"""
        return self.get('/health')

    # Product endpoints
    def get_all_products(self, limit: int = 100) -> List[Dict]:
        """Get all products"""
        result = self.get('/products')
        if isinstance(result, list):
            return result[:limit]
        return []

    def get_product(self, product_id: str) -> Dict[str, Any]:
        """Get product by ID"""
        return self.get(f'/products/{product_id}')

    def search_products_by_name(self, name: str) -> List[Dict]:
        """Search products by name"""
        result = self.get('/products', params={'name': name})
        return result if isinstance(result, list) else []

    def get_products_by_category(self, category: str) -> List[Dict]:
        """Get products by category"""
        result = self.get(f'/products/category/{category}')
        return result if isinstance(result, list) else []

    def get_products_by_brand(self, brand: str) -> List[Dict]:
        """Get products by brand"""
        result = self.get(f'/products/brand/{brand}')
        return result if isinstance(result, list) else []

    # User endpoints
    def get_all_users(self) -> List[Dict]:
        """Get all users"""
        result = self.get('/users')
        return result if isinstance(result, list) else []

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user by ID"""
        return self.get(f'/users/{user_id}')

    def search_users_by_name(self, name: str) -> List[Dict]:
        """Search users by name"""
        result = self.get('/users', params={'name': name})
        return result if isinstance(result, list) else []

    # Inventory endpoints
    def get_inventory(self, product_id: str) -> Dict[str, Any]:
        """Get inventory for a product"""
        return self.get(f'/inventory/{product_id}')

    def get_all_inventory(self) -> List[Dict]:
        """Get all inventory"""
        result = self.get('/inventory')
        return result if isinstance(result, list) else []

    # Order endpoints
    def get_all_orders(self) -> List[Dict]:
        """Get all orders"""
        result = self.get('/orders')
        return result if isinstance(result, list) else []

    def get_order(self, order_id: str) -> Dict[str, Any]:
        """Get order by ID"""
        return self.get(f'/orders/{order_id}')

    def get_user_orders(self, user_id: str) -> List[Dict]:
        """Get orders for a user"""
        result = self.get(f'/orders/user/{user_id}')
        return result if isinstance(result, list) else []

    # Stats endpoints
    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        return self.get('/stats')

    def get_sales_stats(self) -> Dict[str, Any]:
        """Get sales statistics"""
        return self.get('/stats/sales')

    def close(self):
        """Close the session"""
        self.session.close()
