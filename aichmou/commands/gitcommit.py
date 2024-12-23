import click

from aichmou import prompt
from aichmou.args import cli
from aichmou.run import run_args


@cli.command()
@click.pass_context
def gitcommit(ctx):
    """Generate a git commit message"""
    args = ctx.obj["args"]
    pprompt = prompt.GIT_COMMIT

    output = run_args(args, pprompt)
    if output:
        click.echo(output)
