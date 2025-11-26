"""Main entry point for MCP Server with OpenAI API Function Calling"""
import sys
from pathlib import Path

# Add current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from api_client import APIClient
from openai_client import OpenAIClient
from mcp_server import MCPServerFC


def check_dependencies() -> tuple[bool, str]:
    """
    Check if API server and OpenAI API are accessible

    Returns:
        Tuple of (success, message)
    """
    # Check API Server
    api_client = APIClient()
    api_health = api_client.health_check()
    if "error" in api_health:
        return False, f"API Server not accessible: {api_health.get('error')}"

    # Check OpenAI API
    openai_client = OpenAIClient()
    if not openai_client.check_health():
        return False, "OpenAI API not accessible. Make sure your API key is set."

    return True, "All dependencies are healthy"


def print_welcome():
    """Print welcome message"""
    print("\n" + "="*60)
    print("MCP Server - API Data Assistant with OpenAI API")
    print("="*60)
    print("Ask questions about products, users, orders, and more")
    print("Type 'help' for available commands")
    print("Type 'exit' to quit")
    print("="*60 + "\n")

def print_tools(mcp_server: MCPServerFC):
    """Print available tools"""
    tools = mcp_server.get_tools()
    print("\nAvailable tools:")
    print("-" * 60)
    for i, tool in enumerate(tools, 1):
        func = tool.get("function", {})
        print(f"{i}. {func.get('name')}")
        print(f"   Description: {func.get('description')}")
    print("-" * 60 + "\n")


def print_status(api_client: APIClient, openai_client: OpenAIClient):
    """Print status of dependencies"""
    print("\nStatus Check:")
    print("-" * 60)

    # Check API
    api_result = api_client.health_check()
    api_status = "✓ Healthy" if "error" not in api_result else "✗ Error"
    print(f"API Server: {api_status}")

    # Check OpenAI
    openai_status = "✓ Healthy" if openai_client.check_health() else "✗ Not accessible"
    print(f"OpenAI API: {openai_status}")
    print("-" * 60 + "\n")


def main():
    """Main function"""
    print_welcome()

    # Check dependencies
    success, message = check_dependencies()

    if not success:
        print(f"Error: {message}")
        print("\nPlease make sure:")
        print("API Server is running (default: http://localhost:8000)")
        return

    print(f"✓ {message}\n")

    # Initialize API and OpenAI clients
    api_client = APIClient()
    openai_client = OpenAIClient()
    mcp_server = MCPServerFC(api_client, openai_client)

    print(f"Using model: {openai_client.model}")
    print(f"API Server: {api_client.base_url}\n")

    # Main interactive loop
    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # Handle user commands
            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            elif user_input.lower() == "status":
                print_status(api_client, openai_client)
                continue

            elif user_input.lower() == "tools":
                print_tools(mcp_server)
                continue

            # Process message with OpenAI API
            print("\nAssistant: Responding ...", end="\r")
            result = mcp_server.generate_response(user_input)

            # Print response
            print(" " * 50, end="\r")  # Clear the "Responding..." message
            print(f"Assistant: {result['response']}\n")

            # Print tool calls if any were used
            if result.get("used_tools"):
                print(f"[Used tools: {', '.join(result['used_tools'])}]\n")

        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")

    # Clean up resources
    mcp_server.close()


if __name__ == "__main__":
    main()
