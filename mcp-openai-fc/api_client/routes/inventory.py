"""Inventory-related API methods"""


class InventoryMixin:
    """Mixin class for inventory-related operations"""

    def get_inventory(self, threshold: int = None) -> dict:
        """Get all inventory or filter by low stock threshold"""
        try:
            params = {}
            if threshold is not None:
                params['threshold'] = threshold

            response = self.session.get(
                f"{self.base_url}/inventory",
                params=params if params else None,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_product_inventory(self, product_id: str = None, product_name: str = None) -> dict:
        """Get inventory for a specific product by ID or name"""
        # If product_name is provided, search for the product first
        if product_name and not product_id:
            products = self.search_products_by_name(product_name)
            if isinstance(products, list) and len(products) > 0:
                product_id = products[0].get("product_id")
            elif isinstance(products, dict) and "error" not in products:
                product_id = products.get("product_id")
            else:
                return {"error": f"Product '{product_name}' not found"}

        if not product_id:
            return {"error": "Either product_id or product_name must be provided"}

        try:
            response = self.session.get(
                f"{self.base_url}/inventory/{product_id}",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_low_stock_products(self, threshold: int = 20) -> dict:
        """Get all products with low stock"""
        try:
            response = self.session.get(
                f"{self.base_url}/inventory/low-stock",
                params={"threshold": threshold},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
