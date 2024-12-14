#!/usr/bin/env python
# Author: Chmouel Boudjnah <chmouel@chmouel.com>

from mistralai import Mistral
from src.abstract_ai import AbstractAI


class MistralAI(AbstractAI):
    def complete(self, prompt: str, text: str) -> str:
        with Mistral(api_key=self.api_key, server_url=self.server_url) as s:
            res = s.chat.complete(
                model="mistral-large",
                messages=[
                    {
                        "content": prompt % text,
                        "role": "user",
                    },
                ],
            )
            if res is not None:
                return res.choices[0].message.content
        return ""


# Example usage
if __name__ == "__main__":
    from src.common import get_args, get_pass_key, get_prompt, get_text, show_response

    args = get_args()
    prompt = get_prompt(args)
    text = get_text()
    api_key = get_pass_key("github/chmouel-token")

    mistral_ai = MistralAI(
        api_key=api_key, server_url="https://models.inference.ai.azure.com"
    )
    newcontent = mistral_ai.complete(prompt, text)
    show_response(args, text, newcontent)
