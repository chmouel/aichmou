import click

from aichmou import prompt
from aichmou.args import cli
from aichmou.run import run_args


@cli.command()
@click.option("-e", "--english", is_flag=True, help="Set English to True")
@click.pass_context
def spell(ctx, english):
    """Spelling commands"""
    args = ctx.obj["args"]

    pprompt = prompt.SPELL_FR
    if english:
        pprompt = prompt.SPELL_EN

    output = run_args(args, pprompt)
    if output:
        click.echo(output)
