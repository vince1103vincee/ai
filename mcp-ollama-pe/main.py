"""Main entry point for MCP Server with Ollama integration"""
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from api_client import APIClient
from ollama_client import OllamaClient
from mcp_server import MCPServer


def check_dependencies() -> tuple[bool, str]:
    """
    Check if API server and Ollama are accessible

    Returns:
        Tuple of (success, message)
    """
    # Check API Server
    api_client = APIClient()
    api_health = api_client.health_check()
    if "error" in api_health:
        return False, f"API Server not accessible: {api_health.get('error')}"

    # Check Ollama
    ollama_client = OllamaClient()
    if not ollama_client.check_health():
        return False, "Ollama not accessible. Make sure it's running on the configured address."

    return True, "All dependencies are healthy"


def print_welcome():
    """Print welcome message"""
    print("\n" + "="*60)
    print("MCP Server - API Data Assistant with Ollama2")
    print("="*60)
    print("Ask questions about products, users, orders, and inventory")
    print("Type 'help' for available commands")
    print("Type 'exit' to quit")
    print("="*60 + "\n")


def print_help():
    """Print help information"""
    print("\nAvailable commands:")
    print("  help              - Show this help message")
    print("  status            - Check API and Ollama status")
    print("  tools             - List available tools")
    print("  exit              - Exit the program")
    print("\nExamples:")
    print("  What products do you have?")
    print("  Show me all iphones")
    print("  How many users are in the system?")
    print("  What orders were placed by user u001?")
    print("  What's the current inventory status?")
    print()


def print_tools(mcp_server: MCPServer):
    """Print available tools"""
    tools = mcp_server.get_tools()
    print("\nAvailable tools:")
    print("-" * 60)
    for i, tool in enumerate(tools, 1):
        print(f"{i}. {tool['name']}")
        print(f"   Description: {tool['description']}")
    print("-" * 60 + "\n")


def print_status(api_client: APIClient, ollama_client: OllamaClient):
    """Print status of dependencies"""
    print("\nStatus Check:")
    print("-" * 60)

    # Check API
    api_result = api_client.health_check()
    api_status = "✓ Healthy" if "error" not in api_result else "✗ Error"
    print(f"API Server: {api_status}")

    # Check Ollama
    ollama_status = "✓ Healthy" if ollama_client.check_health() else "✗ Not accessible"
    print(f"Ollama: {ollama_status}")
    print("-" * 60 + "\n")


def main():
    """Main function"""
    print_welcome()

    # Check dependencies
    success, message = check_dependencies()

    if not success:
        print(f"Error: {message}")
        print("\nPlease make sure:")
        print("1. API Server is running (default: http://localhost:8000)")
        print("2. Ollama is running (default: http://localhost:11434)")
        return

    print(f"✓ {message}\n")

    # Initialize clients
    api_client = APIClient()
    ollama_client = OllamaClient()
    mcp_server = MCPServer(api_client, ollama_client)

    print(f"Using model: {ollama_client.model}")
    print(f"API Server: {api_client.base_url}\n")

    # Interactive loop
    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            elif user_input.lower() == "help":
                print_help()
                continue

            elif user_input.lower() == "status":
                print_status(api_client, ollama_client)
                continue

            elif user_input.lower() == "tools":
                print_tools(mcp_server)
                continue

            # Process user message
            print("\nAssistant: Thinking...", end="\r")
            result = mcp_server.generate_response(user_input)

            # Print response
            print(" " * 50, end="\r")  # Clear the "Thinking..." message
            print(f"Assistant: {result['response']}\n")

            # Print tool info if tools were used
            if result.get("used_tools"):
                print(f"[Used tools: {', '.join(result['used_tools'])}]\n")

        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")

    # Cleanup
    mcp_server.close()


if __name__ == "__main__":
    main()
