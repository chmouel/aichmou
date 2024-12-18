#!/usr/bin/env python
# Author: Chmouel Boudjnah <chmouel@chmouel.com>

from openai import OpenAI as _OpenAI
from .abstract_ai import AbstractAI


class OpenAI(AbstractAI):
    def complete(self, prompt: str, text: str) -> str:
        client = _OpenAI(
            base_url=self.server_url,
            api_key=self.api_key,
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
            model="gpt-4o-mini",
            temperature=1,
            max_tokens=4096,
            top_p=1,
        )
        return response.choices[0].message.content
