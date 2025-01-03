import click

from aichmou import prompt as default_prompts
from aichmou import run
from aichmou.args import cli


@cli.command()
@click.pass_context
def prompt(ctx):
    """Free prompt from an helpful assistant"""
    args = ctx.obj["args"]
    args.editor = True

    output = run.args(args, default_prompts.DEFAULT)
    if output:
        click.echo(output)
