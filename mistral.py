#!/usr/bin/env python
# Author: Chmouel Boudjnah <chmouel@chmouel.com>

from mistralai import Mistral

from common import get_args, get_pass_key, get_prompt, get_text, show_response

args = get_args()
prompt = get_prompt(args)
text = get_text()
api_key = get_pass_key("github/chmouel-token")

with Mistral(
    api_key=api_key,
    server_url="https://models.inference.ai.azure.com",
) as s:
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
        newcontent = res.choices[0].message.content
        show_response(args, text, res.choices[0].message.content)
