import requests
import json
from devcrew_ai.llm.base import BaseLLM
from devcrew_ai.config import OLLAMA_API_URL, OLLAMA_MODEL

class OllamaLLM(BaseLLM):
    def __init__(self, api_url: str = OLLAMA_API_URL, model: str = OLLAMA_MODEL):
        self.api_url = api_url
        self.model = model

    def generate(self, prompt: str, system_instruction: str = "") -> str:
        """
        Generate text offline using a local Ollama instance.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_instruction,
            "stream": False,
            "options": {
                "temperature": 0.2
            }
        }
        
        try:
            print(f"[Ollama] Sending request to model '{self.model}' at url '{self.api_url}'...")
            response = requests.post(
                self.api_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=90  # Generous timeout for local models running on CPU/GPU
            )
            
            if response.status_code == 200:
                result_json = response.json()
                return result_json.get("response", "")
            else:
                err_msg = f"Ollama returned status code {response.status_code}: {response.text}"
                print(f"[Ollama Error] {err_msg}")
                return f"[Ollama Error] Could not generate response. Server returned {response.status_code}."
                
        except requests.exceptions.RequestException as e:
            print(f"[Ollama Connection Error] Failsafe fallback to Mock LLM. Connection failed: {e}")
            return f"[Ollama Error] Failed to connect to local Ollama server at {self.api_url}. Is Ollama running?"
