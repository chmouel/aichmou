import sys

from . import common
from .providers.azure import AzureAI
from .providers.chatgpt import ChatGPT
from .providers.gemini import Gemini
from .providers.groq import Groq
from .providers.mistral import MistralAI
from .providers.openai import OpenAI


def fallover(args, prompt, api_key, text, orders=None):
    orders = orders or common.DEFAULT_ORDERS
    newcontent = None

    for order in orders:
        try:
            if order == "chatgpt":
                ai = ChatGPT(api_key=None, server_url=args.openai_api_url)

            elif order == "gemini":
                ai = Gemini(
                    api_key="pass::" + args.gemini_api_pass_key, server_url=None
                )
            elif order == "azureai":
                ai = AzureAI(api_key=api_key, server_url=common.SERVER_URL)
            elif order == "openai":
                ai = OpenAI(api_key=api_key, server_url=common.SERVER_URL)
            elif order == "mistralai":
                ai = MistralAI(api_key=api_key, server_url=common.SERVER_URL)
            elif order == "groq":
                ai = Groq(api_key="pass::" + args.groq_api_pass_key, server_url=None)
            newcontent = ai.complete(prompt, text)
            if newcontent:
                break
        except Exception as e:
            sys.stderr.write(f"{order.capitalize()} failed: {e}\n")

    if not newcontent:
        sys.stderr.write("All failed, exiting\n")
        sys.exit(1)

    return common.show_response(args, text, newcontent)


def args(args, prompt, text=None):
    text = text or common.get_text(args)
    api_key = common.get_pass_key(args.github_api_pass_key)
    if args.mistral:
        ai = MistralAI(api_key=api_key, server_url=common.SERVER_URL)
    elif args.gemini:
        ai = Gemini(api_key="pass::" + args.gemini_api_pass_key, server_url=None)
    elif args.azure:
        ai = AzureAI(api_key=api_key, server_url=common.SERVER_URL)
    elif args.groq:
        ai = Groq(api_key="pass::" + args.groq_api_pass_key, server_url=None)
    elif args.openai:
        ai = OpenAI(api_key=api_key, server_url=args.openai_api_url, model=args.model)
    elif args.chatgpt:
        ai = ChatGPT(api_key=None, server_url=None)
    else:
        return fallover(args, prompt, api_key, text)

    newcontent = ai.complete(prompt, text)
    return common.show_response(args, text, newcontent)
