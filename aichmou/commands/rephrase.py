import click

from aichmou import prompt, run
from aichmou.args import cli


@cli.command()
@click.pass_context
def rephrase(ctx):
    """Rephrase sentence for buisiness"""
    args = ctx.obj["args"]

    pprompt = prompt.BUISNESS_REPHRASE
    output = run.args(args, pprompt)
    if output:
        click.echo(output)
