"""MCP Server implementation"""
import json
from typing import Any, Dict, List, Optional
from api_client import APIClient
from ollama_client import OllamaClient
from .tools import APITools


class MCPServer:
    """MCP Server for API data assistant"""

    def __init__(self, api_client: APIClient, ollama_client: OllamaClient):
        self.api_client = api_client
        self.ollama_client = ollama_client
        self.tools = APITools(api_client)

    def get_tools(self) -> List[Dict[str, Any]]:
        """Get available tools"""
        return self.tools.get_tools()

    def process_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        Process a tool call and return the result

        Args:
            tool_name: Name of the tool
            arguments: Tool arguments

        Returns:
            JSON string with the result
        """
        return self.tools.execute_tool(tool_name, arguments)

    def get_tool_context_prompt(self) -> str:
        """Get a prompt that describes available tools"""
        tools = self.get_tools()
        tools_json = json.dumps(tools, indent=2)

        return f"""You are an AI assistant that helps users query and analyze product data from an e-commerce system.

You have access to the following tools:
{tools_json}

IMPORTANT: When you need to call a tool, respond with EXACTLY this format (nothing else on that line):
<tool_call>
{{"name": "tool_name", "arguments": {{"param1": "value1"}}}}
</tool_call>

Then explain the results.

Example:
User: "What Apple products do you have?"
<tool_call>
{{"name": "get_products_by_brand", "arguments": {{"brand": "Apple"}}}}
</tool_call>
Based on the search results, Apple has the following products..."""

    def generate_response(self, user_message: str) -> Dict[str, Any]:
        """
        Generate a response to user message, potentially using tools

        Args:
            user_message: The user's message

        Returns:
            Dict with 'response' and 'used_tools' keys
        """
        # Build system prompt
        system_prompt = self.get_tool_context_prompt()

        # Create messages for Ollama (no conversation history, just current message)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]

        # Get initial response from Ollama
        ollama_result = self.ollama_client.chat(messages, stream=False)
        initial_response = ollama_result.get("response", "")

        used_tools = []
        tool_results = {}

        # Extract tool calls from response
        tool_calls = self._extract_tool_calls(initial_response)

        if tool_calls:
            for tool_call in tool_calls:
                tool_name = tool_call.get("name")
                arguments = tool_call.get("arguments", {})

                try:
                    result = self.process_tool_call(tool_name, arguments)
                    tool_results[tool_name] = json.loads(result)
                    used_tools.append(tool_name)
                except Exception as e:
                    tool_results[tool_name] = {"error": str(e)}

        # If tools were used, generate a final response with the tool results
        final_response = initial_response
        if tool_results:
            # Build a message with tool results
            tool_results_str = json.dumps(tool_results, indent=2)
            tool_context_msg = f"Based on the tool results:\n{tool_results_str}"

            # Create new messages with tool results (still no history)
            final_messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
                {"role": "user", "content": tool_context_msg}
            ]

            final_result = self.ollama_client.chat(final_messages, stream=False)
            final_response = final_result.get("response", "")

        return {
            "response": final_response,
            "used_tools": used_tools,
            "tool_results": tool_results if tool_results else None
        }

    def _extract_tool_calls(self, response: str) -> List[Dict[str, Any]]:
        """
        Extract tool calls from response marked with <tool_call>...</tool_call>

        Returns:
            List of tool calls
        """
        import re
        tool_calls = []

        # Look for <tool_call>...</tool_call> blocks
        pattern = r'<tool_call>\s*(\{.*?\})\s*</tool_call>'
        matches = re.findall(pattern, response, re.DOTALL)

        for match in matches:
            try:
                obj = json.loads(match)
                if "name" in obj:
                    tool_calls.append({
                        "name": obj["name"],
                        "arguments": obj.get("arguments", {})
                    })
            except json.JSONDecodeError:
                pass

        return tool_calls

    def close(self):
        """Close all connections"""
        self.api_client.close()
