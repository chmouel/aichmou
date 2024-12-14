#!/usr/bin/env python
# Author: Chmouel Boudjnah <chmouel@chmouel.com>
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

from common import get_args, get_pass_key, get_prompt, get_text, show_response

args = get_args()
api_key = get_pass_key("github/chmouel-token")
prompt = get_prompt(args)
text = get_text()

# To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings.
# Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
client = ChatCompletionsClient(
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential(api_key),
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


show_response(args, text, response.choices[0].message.content)
