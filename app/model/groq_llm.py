from langchain.llms.base import LLM
from typing import Optional, List
from groq import Groq
from pydantic import PrivateAttr

class GroqLLM(LLM):
    _client: Groq = PrivateAttr()
    api_key: str
    model_name: str = "llama-3.3-70b-versatile"

    def __init__(self, **data):
        super().__init__(**data)
        self._client = Groq(api_key=self.api_key)

    @property
    def _llm_type(self) -> str:
        return "groq_llm"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self._client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            stop=stop,
        )
        return response.choices[0].message.content
