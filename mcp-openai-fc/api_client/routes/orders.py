"""Order-related API methods"""


class OrdersMixin:
    """Mixin class for order-related operations"""

    def get_all_orders(self) -> dict:
        """Get all orders"""
        try:
            response = self.session.get(
                f"{self.base_url}/orders",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
