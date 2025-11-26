"""Base HTTP client utilities"""
import requests
from config import API_SERVER_URL, API_SERVER_TIMEOUT


class BaseClient:
    """Base client with session management"""

    def __init__(self, base_url=API_SERVER_URL, timeout=API_SERVER_TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def health_check(self) -> dict:
        """Check if API server is healthy"""
        try:
            response = self.session.get(
                f"{self.base_url}/health",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def close(self):
        """Close the session"""
        self.session.close()
