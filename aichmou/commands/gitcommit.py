import click

from aichmou import prompt, run
from aichmou.args import cli


@cli.command()
@click.pass_context
def gitcommit(ctx):
    """Generate a git commit message"""
    args = ctx.obj["args"]
    args.orders = run.DEFAULT_ORDERS
    args.orders.remove("openai")
    args.orders.insert(0, "openai")
    pprompt = prompt.GIT_COMMIT

    output = run.args(args, pprompt)
    if output:
        click.echo(output)
