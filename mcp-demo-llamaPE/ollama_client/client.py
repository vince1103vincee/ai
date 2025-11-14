"""Ollama Client for generating responses using local LLM"""
import requests
import json
from typing import Optional, Dict, Any
from config.settings import OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_TEMPERATURE


class OllamaClient:
    """Client for interacting with Ollama"""

    def __init__(
        self,
        base_url: str = OLLAMA_BASE_URL,
        model: str = OLLAMA_MODEL,
        temperature: float = OLLAMA_TEMPERATURE
    ):
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.temperature = temperature

    def check_health(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def generate(
        self,
        prompt: str,
        stream: bool = False,
        context: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Generate response using Ollama

        Args:
            prompt: The input prompt
            stream: Whether to stream the response
            context: Optional context from previous response

        Returns:
            Response dict with 'response' and optional 'context' fields
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": stream,
                "temperature": self.temperature
            }

            if context:
                payload["context"] = context

            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            response.raise_for_status()

            if stream:
                # Handle streaming response
                full_response = ""
                context_data = None
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        full_response += chunk.get("response", "")
                        context_data = chunk.get("context")

                return {
                    "response": full_response.strip(),
                    "context": context_data
                }
            else:
                data = response.json()
                return {
                    "response": data.get("response", "").strip(),
                    "context": data.get("context")
                }

        except requests.exceptions.RequestException as e:
            return {"response": f"Error: {str(e)}", "context": None}

    def chat(
        self,
        messages: list,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Chat with Ollama using conversation history

        Args:
            messages: List of message dicts with 'role' and 'content'
            stream: Whether to stream the response

        Returns:
            Response dict with 'response' field
        """
        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": stream,
                "temperature": self.temperature
            }

            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=60
            )
            response.raise_for_status()

            if stream:
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        full_response += chunk.get("message", {}).get("content", "")

                return {"response": full_response.strip()}
            else:
                data = response.json()
                return {"response": data.get("message", {}).get("content", "").strip()}

        except requests.exceptions.RequestException as e:
            return {"response": f"Error: {str(e)}"}
