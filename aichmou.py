#!/usr/bin/env python
# Author: Chmouel Boudjnah <chmouel@chmouel.com>

from aichmou.azure import AzureAI
from aichmou.common import (get_args, get_pass_key, get_prompt, get_text,
                            show_response)
from aichmou.mistral import MistralAI


def main():
    args = get_args()
    prompt = get_prompt(args)
    text = get_text()
    api_key = get_pass_key("github/chmouel-token")

    if args.mistral:
        ai = MistralAI(
            api_key=api_key, server_url="https://models.inference.ai.azure.com"
        )
    else:
        ai = AzureAI(
            api_key=api_key,
            server_url="https://models.inference.ai.azure.com",
        )

    newcontent = ai.complete(prompt, text)
    show_response(args, text, newcontent)


if __name__ == "__main__":
    main()
