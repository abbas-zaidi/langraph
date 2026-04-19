import requests
from app.config import settings

class DeepSeekClient:
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.base_url = settings.BASE_URL
        self.model = settings.MODEL_NAME

    def chat(self, messages):
        url = f"{self.base_url}/chat/completions"

        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
            },
        )

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]