"""Tool definitions for Function Calling"""
import json
import os
from api_client import APIClient


class APITools:
    """API Tools for Function Calling"""

    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.tools_data = self._load_tools()
        self.tool_map = self._build_tool_map()

    def _load_tools(self) -> list:
        """Load tools definition from tools.json file"""
        tools_file = os.path.join(os.path.dirname(__file__), "tools.json")
        try:
            with open(tools_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: tools.json not found at {tools_file}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error parsing tools.json: {e}")
            return []

    def _build_tool_map(self) -> dict:
        """Build a dynamic tool map from tools.json and link to api_client methods"""
        tool_map = {}
        for tool in self.tools_data:
            # Extract tool name from tools.json
            tool_name = tool.get("function", {}).get("name")

            # Check if api_client has this method
            if tool_name and hasattr(self.api_client, tool_name):
                tool_map[tool_name] = getattr(self.api_client, tool_name)

        return tool_map

    def get_tools(self) -> list:
        """Return tools definition for Function Calling"""
        return self.tools_data

    def execute_tool(self, tool_name: str, arguments: dict) -> str:
        """Execute a tool and return the result as JSON string"""
        try:
            # Parse arguments if it's a string
            if isinstance(arguments, str):
                arguments = json.loads(arguments)

            # Check if tool exists in the map
            if tool_name not in self.tool_map:
                return json.dumps({"error": f"Unknown tool: {tool_name}"})

            # Get the method from the map and execute it
            tool_method = self.tool_map[tool_name]
            result = tool_method(**arguments)

            return json.dumps(result)
        except Exception as e:
            return json.dumps({"error": str(e)})
