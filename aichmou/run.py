import sys

from . import common
from .providers.azure import AzureAI
from .providers.chatgpt import ChatGPT
from .providers.gemini import Gemini
from .providers.groq import Groq
from .providers.mistral import MistralAI
from .providers.openai import OpenAI

SERVER_URL = "https://models.inference.ai.azure.com"


def fallover(args, prompt, api_key, text):
    try:
        ai = ChatGPT(api_key=None, server_url=None)
        newcontent = ai.complete(prompt, text)
    except Exception as e:
        sys.stderr.write(f"ChatGPT failed: {e}\n")

    try:
        ai = Gemini(api_key="pass::" + args.gemini_api_pass_key, server_url=None)
        newcontent = ai.complete(prompt, text)
    except Exception as e:
        sys.stderr.write(f"Gemini failed: {e}\n")

    try:
        ai = AzureAI(api_key=api_key, server_url=SERVER_URL)
        newcontent = ai.complete(prompt, text)
    except Exception as e:
        sys.stderr.write(f"AzureAI failed: {e}\n")

    if not newcontent:
        try:
            ai = OpenAI(api_key=api_key, server_url=SERVER_URL)
            newcontent = ai.complete(prompt, text)
        except Exception as e:
            sys.stderr.write(f"OpenAI failed: {e}\n")

    if not newcontent:
        try:
            ai = MistralAI(api_key=api_key, server_url=SERVER_URL)
            newcontent = ai.complete(prompt, text)
        except Exception as e:
            sys.stderr.write(f"MistralAI failed: {e}\n")

    if not newcontent:
        try:
            ai = Groq(api_key="pass::" + args.groq_api_pass_key, server_url=None)
            newcontent = ai.complete(prompt, text)
        except Exception as e:
            sys.stderr.write(f"Groq failed: {e}\n")

    if not newcontent:
        sys.stderr.write("All failed, exiting\n")
        sys.exit(1)

    return common.show_response(args, text, newcontent)


def run_args(args, prompt):
    text = common.get_text()
    api_key = common.get_pass_key(args.github_api_pass_key)
    if args.mistral:
        ai = MistralAI(api_key=api_key, server_url=SERVER_URL)
    elif args.gemini:
        ai = Gemini(api_key="pass::" + args.gemini_api_pass_key, server_url=None)
    elif args.azure:
        ai = AzureAI(api_key=api_key, server_url=SERVER_URL)
    elif args.groq:
        ai = Groq(api_key="pass::" + args.groq_api_pass_key, server_url=None)
    elif args.openai:
        ai = OpenAI(api_key=api_key, server_url=SERVER_URL)
    elif args.chatgpt:
        ai = ChatGPT(api_key=None, server_url=None)
    else:
        return fallover(args, prompt, api_key, text)

    newcontent = ai.complete(prompt, text)
    return common.show_response(args, text, newcontent)
