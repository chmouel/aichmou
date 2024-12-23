import click

from . import run


class DictToObject:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)


@click.group()
@click.option(
    "--github-api-pass-key",
    default="github/chmouel-token",
    help="GitHub API Key in pass store",
)
@click.option("-N", "--no-output", is_flag=True, help="Do not show output")
@click.option("--git-commit", is_flag=True, help="Generate a Git commit message")
@click.option(
    "-g",
    "--graphical-diff",
    is_flag=True,
    default=False,
    help="Do graphical diff with kitty",
)
@click.option(
    "-t", "--text-diff", is_flag=True, default=False, help="Show diff with git diff"
)
@click.option("-n", "--no-diff", is_flag=True, default=True, help="No diff output")
@click.option(
    "-C", "--no-clipboard-copy", is_flag=True, default=False, help="No clipboard copy"
)
@click.option("--mistral", is_flag=True, default=False, help="Use mistral")
@click.option("--azure", is_flag=True, default=False, help="Use Azure")
@click.option("--openai", is_flag=True, default=False, help="Use OpenAI")
@click.option(
    "--chatgpt",
    is_flag=True,
    default=False,
    help="Use ChatGPT (need the gh-gpt command installed in path and configured)",
)
@click.option("--groq", is_flag=True, default=False, help="Use Groq")
@click.option(
    "--groq-api-pass-key", default="groq/api", help="Groq API Key in pass store"
)
@click.option("--gemini", is_flag=True, default=False, help="Use Groq")
@click.option(
    "--gemini-api-pass-key",
    default="google/gemini-api",
    help="Gemini API Key in pass store",
)
@click.pass_context
def cli(ctx, *_args, **_kwargs):
    ctx.ensure_object(dict)
    _kwargs["orders"] = run.DEFAULT_ORDERS
    ctx.obj["args"] = DictToObject(_kwargs)
    return _args, _kwargs
