#!/usr/bin/env python
# Author: Chmouel Boudjnah <chmouel@chmouel.com>

from groq import Groq as _Groq

from aichmou.common import get_pass_key

from .abstract_ai import AbstractAI


class Groq(AbstractAI):
    model = "llama3-8b-8192"
    temperature = 1
    max_tokens = 100

    def complete(self, prompt: str, text: str) -> str:
        server_url = self.server_url or None
        api_key = self.api_key
        if self.api_key.startswith("pass::"):
            api_key = get_pass_key(self.api_key.split("::")[1])
        client = _Groq(
            base_url=server_url,
            api_key=api_key,
        )
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {
                    "content": text,
                    "role": "user",
                },
            ],
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content
