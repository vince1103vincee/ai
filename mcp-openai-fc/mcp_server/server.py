"""MCP Server with native Function Calling"""
import json
from typing import Any, Dict, List
from api_client import APIClient
from openai_client import OpenAIClient
from .tools import APITools


class MCPServerFC:
    """MCP Server with native Function Calling support"""

    def __init__(self, api_client: APIClient, openai_client: OpenAIClient):
        self.api_client = api_client
        self.openai_client = openai_client
        self.tools = APITools(api_client)

    def get_tools(self) -> List[Dict[str, Any]]:
        """Get tools for Function Calling"""
        return self.tools.get_tools()

    def process_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Process a tool call and return the result"""
        return self.tools.execute_tool(tool_name, arguments)

    def generate_response(self, user_message: str) -> Dict[str, Any]:
        # Build system prompt
        system_prompt = """You are an AI assistant that helps users query and analyze product data from an e-shop system.

You have access to several tools to query the API. Use them when needed to answer user questions about products, users, inventories and orders.

When the user asks a question that requires data, use the appropriate tool to fetch the data and then provide a helpful response based on the results."""

        # Create messages for OpenAI
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]

        # Get available tools
        tools = self.get_tools()

        # Call OpenAI API with Function Calling
        openai_result = self.openai_client.chat_with_tools(messages, tools)

        if "error" in openai_result:
            return {
                "response": f"Error: {openai_result['error']}",
                "used_tools": [],
                "tool_results": None
            }

        initial_response = openai_result.get("response", "")
        tool_calls = openai_result.get("tool_calls", [])

        used_tools = []
        tool_results = {}

        # Process tool calls if any
        if tool_calls:
            for tool_call in tool_calls:
                tool_name = tool_call.get("name")
                arguments = tool_call.get("arguments", {})

                try:
                    # Parse arguments if it's a string
                    if isinstance(arguments, str):
                        arguments = json.loads(arguments)

                    result = self.process_tool_call(tool_name, arguments)
                    tool_results[tool_name] = json.loads(result)
                    used_tools.append(tool_name)
                except Exception as e:
                    tool_results[tool_name] = {"error": str(e)}

        # If tools were used, generate a final response with tool results
        final_response = initial_response
        if tool_results:
            # Build messages with tool results for follow-up
            tool_results_str = json.dumps(tool_results, indent=2)
            tool_context_msg = f"Based on the tool results:\n{tool_results_str}\n\nPlease provide a helpful answer to the user's original question."

            # Create new messages with tool results
            final_messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": initial_response},
                {"role": "user", "content": tool_context_msg}
            ]

            final_result = self.openai_client.chat(final_messages, stream=False)
            if "error" not in final_result:
                final_response = final_result.get("response", initial_response)

        return {
            "response": final_response,
            "used_tools": used_tools,
            "tool_results": tool_results if tool_results else None
        }

    def close(self):
        """Close all connections"""
        self.api_client.close()
