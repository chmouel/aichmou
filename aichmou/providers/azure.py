#!/usr/bin/env python
# Author: Chmouel Boudjnah <chmouel@chmouel.com>

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

from .abstract_ai import AbstractAI


class AzureAI(AbstractAI):
    def complete(self, prompt: str, text: str) -> str:
        client = ChatCompletionsClient(
            endpoint=self.server_url,
            credential=AzureKeyCredential(self.api_key),
        )
        response = client.complete(
            messages=[
                SystemMessage(content=prompt),
                UserMessage(content=text),
            ],
            model="Llama-3.3-70B-Instruct",
            temperature=0.8,
            max_tokens=2048,
            top_p=0.1,
        )
        return response.choices[0].message.content


# Example usage
if __name__ == "__main__":
    from src.common import get_args, get_pass_key, get_prompt, get_text, show_response

    args = get_args()
    prompt = get_prompt(args)
    text = get_text()
    api_key = get_pass_key("github/chmouel-token")

    azure_ai = AzureAI(
        api_key=api_key, server_url="https://models.inference.ai.azure.com"
    )
    newcontent = azure_ai.complete(prompt, text)
    show_response(args, text, newcontent)
