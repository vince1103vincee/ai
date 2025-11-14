"""Tool definitions for MCP Server"""
from typing import Any, Dict, List
from api_client import APIClient
from pathlib import Path
import json
import yaml


class APITools:
    """Tools for querying API Server data"""

    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.tools = self._load_tools()

    def _load_tools(self) -> List[Dict[str, Any]]:
        """Load tools from YAML file"""
        tools_file = Path(__file__).parent / "tools.yaml"
        try:
            with open(tools_file, 'r') as f:
                data = yaml.safe_load(f)
                return data.get("tools", [])
        except Exception as e:
            print(f"Error loading tools.yaml: {e}")
            return []

    def get_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools"""
        return self.tools

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        Execute a tool with given arguments

        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments for the tool

        Returns:
            JSON string with the result
        """
        try:
            if tool_name == "get_all_products":
                limit = arguments.get("limit", 100)
                result = self.api_client.get_all_products(limit=limit)
                return json.dumps({"success": True, "data": result})

            elif tool_name == "get_product":
                product_id = arguments.get("product_id")
                result = self.api_client.get_product(product_id)
                return json.dumps({"success": True, "data": result})

            elif tool_name == "search_products_by_name":
                name = arguments.get("name")
                result = self.api_client.search_products_by_name(name)
                return json.dumps({"success": True, "data": result})

            elif tool_name == "get_products_by_category":
                category = arguments.get("category")
                result = self.api_client.get_products_by_category(category)
                return json.dumps({"success": True, "data": result})

            elif tool_name == "get_products_by_brand":
                brand = arguments.get("brand")
                result = self.api_client.get_products_by_brand(brand)
                return json.dumps({"success": True, "data": result})

            elif tool_name == "get_inventory":
                product_id = arguments.get("product_id")
                result = self.api_client.get_inventory(product_id)
                return json.dumps({"success": True, "data": result})

            elif tool_name == "get_all_users":
                result = self.api_client.get_all_users()
                return json.dumps({"success": True, "data": result})

            elif tool_name == "get_user":
                user_id = arguments.get("user_id")
                result = self.api_client.get_user(user_id)
                return json.dumps({"success": True, "data": result})

            elif tool_name == "search_users_by_name":
                name = arguments.get("name")
                result = self.api_client.search_users_by_name(name)
                return json.dumps({"success": True, "data": result})

            elif tool_name == "get_all_orders":
                result = self.api_client.get_all_orders()
                return json.dumps({"success": True, "data": result})

            elif tool_name == "get_order":
                order_id = arguments.get("order_id")
                result = self.api_client.get_order(order_id)
                return json.dumps({"success": True, "data": result})

            elif tool_name == "get_user_orders":
                user_id = arguments.get("user_id")
                result = self.api_client.get_user_orders(user_id)
                return json.dumps({"success": True, "data": result})

            elif tool_name == "get_stats":
                result = self.api_client.get_stats()
                return json.dumps({"success": True, "data": result})

            elif tool_name == "api_health_check":
                result = self.api_client.health_check()
                return json.dumps({"success": True, "data": result})

            else:
                return json.dumps({"success": False, "error": f"Unknown tool: {tool_name}"})

        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})
