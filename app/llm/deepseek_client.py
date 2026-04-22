import requests
from langchain_openai import ChatOpenAI
from app.config import settings

class DeepSeekClient:
    _instance = None  # class variable to hold the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # This will run every time someone calls DeepSeekClient(), but the
        # instance is the same. To avoid reinitializing, we guard with a flag.
        if not hasattr(self, '_initialized'):
            self.api_key = settings.DEEPSEEK_API_KEY
            self.base_url = settings.BASE_URL
            self.model = settings.MODEL_NAME
            self._initialized = True

    # def __init__(self):
    #     self.api_key = settings.DEEPSEEK_API_KEY
    #     self.base_url = settings.BASE_URL
    #     self.model = settings.MODEL_NAME

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
    
    def get_model(self):
        return ChatOpenAI(
            model=self.model,  # or "deepseek-reasoner"
            openai_api_key= self.api_key,  # or set DEEPSEEK_API_KEY env var
            openai_api_base=self.base_url,  # DeepSeek's OpenAI-compatible endpoint
            temperature=0.7,
            max_tokens=1000,
        )