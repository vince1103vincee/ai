"""OpenAI API Client with Function Calling support"""
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE


class OpenAIClient:
    """Client for OpenAI API with native Function Calling support"""

    def __init__(self, api_key=OPENAI_API_KEY, model=OPENAI_MODEL, temperature=OPENAI_TEMPERATURE):
        """Initialize OpenAI client"""
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.client = OpenAI(api_key=api_key)

    def check_health(self) -> bool:
        """Check if OpenAI API is accessible"""
        try:
            self.client.models.list()
            return True
        except Exception as e:
            print(f"OpenAI API health check failed: {e}")
            return False

    def chat(self, messages: list, stream: bool = False) -> dict:
        """Send chat message to OpenAI (without Function Calling)"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                stream=stream
            )
            if stream:
                return {"response": response}
            else:
                return {"response": response.choices[0].message.content}
        except Exception as e:
            return {"error": str(e)}

    def chat_with_tools(self, messages: list, tools: list) -> dict:
        """Send chat message with Function Calling support"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=self.temperature
            )

            result = {
                "response": response.choices[0].message.content or "",
                "tool_calls": []
            }

            # Extract tool calls if any
            if response.choices[0].message.tool_calls:
                for tool_call in response.choices[0].message.tool_calls:
                    result["tool_calls"].append({
                        "id": tool_call.id,
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    })

            return result
        except Exception as e:
            return {"error": str(e), "tool_calls": []}
