"""User-related API methods"""


class UsersMixin:
    """Mixin class for user-related operations"""

    def get_all_users(self) -> dict:
        """Get all users"""
        try:
            response = self.session.get(
                f"{self.base_url}/users",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_user(self, user_id: str) -> dict:
        """Get user by ID"""
        try:
            response = self.session.get(
                f"{self.base_url}/users/{user_id}",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def search_users_by_name(self, name: str) -> dict:
        """Search users by name with case-insensitive partial match"""
        try:
            response = self.session.get(
                f"{self.base_url}/users",
                params={"name": name},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def search_users_by_email(self, email: str) -> dict:
        """Search users by email address with case-insensitive match"""
        try:
            response = self.session.get(
                f"{self.base_url}/users",
                params={"email": email},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_user_orders(self, user_id: str = None, user_name: str = None) -> dict:
        """Get all orders for a specific user by ID or name"""
        # If user_name is provided, search for the user first
        if user_name and not user_id:
            users = self.search_users_by_name(user_name)
            if isinstance(users, list) and len(users) > 0:
                user_id = users[0].get("user_id")
            elif isinstance(users, dict) and "error" not in users:
                user_id = users.get("user_id")
            else:
                return {"error": f"User '{user_name}' not found"}

        if not user_id:
            return {"error": "Either user_id or user_name must be provided"}

        try:
            response = self.session.get(
                f"{self.base_url}/orders/user/{user_id}",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
