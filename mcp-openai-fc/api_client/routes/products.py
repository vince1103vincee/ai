"""Product-related API methods"""


class ProductsMixin:
    """Mixin class for product-related operations"""

    def get_all_products(self, limit: int = 100) -> dict:
        """Get all products"""
        try:
            response = self.session.get(
                f"{self.base_url}/products",
                params={"limit": limit},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_product(self, product_id: str) -> dict:
        """Get product by ID"""
        try:
            response = self.session.get(
                f"{self.base_url}/products/{product_id}",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def search_products_by_name(self, name: str) -> dict:
        """Search products by name with case-insensitive partial match"""
        try:
            response = self.session.get(
                f"{self.base_url}/products",
                params={"name": name},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def search_products_by_brand(self, brand: str) -> dict:
        """Search products by brand"""
        try:
            response = self.session.get(
                f"{self.base_url}/products",
                params={"brand": brand},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def search_products_by_category(self, category: str) -> dict:
        """Search products by category"""
        try:
            response = self.session.get(
                f"{self.base_url}/products",
                params={"category": category},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
