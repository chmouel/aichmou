import os
import subprocess
import sys

import click

from aichmou import common, prompt, run
from aichmou.args import cli


class GitError(Exception):
    """Exception raised for errors in the git command"""

    pass


def git_commit(commit_message):
    """Commit the changes with the given commit message"""
    try:
        subprocess.check_output(["git", "add", "."])
        subprocess.check_output(["git", "commit", "-S", "-m", commit_message])
        os.system("git commit --amend")
    except subprocess.CalledProcessError as e:
        raise GitError(f"An error occurred while committing the changes: {e}")


def get_diff_from_staged_unstaged():
    """Get a diff from the staged or unstaged changes"""
    try:
        subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"])
    except subprocess.CalledProcessError:
        raise GitError("Not a git repository")

    try:
        # Get the diff for staged changes
        staged_diff = subprocess.check_output(["git", "diff", "--cached"]).decode(
            "utf-8"
        )

        # Get the diff for unstaged changes
        unstaged_diff = subprocess.check_output(["git", "diff"]).decode("utf-8")

        return staged_diff + unstaged_diff
    except subprocess.CalledProcessError as e:
        return f"An error occurred while getting the diff: {e}"


@cli.command()
@click.option(
    "-c",
    "--commit",
    default=False,
    is_flag=True,
    help="Generate commit from the current directory",
)
@click.pass_context
def gitcommit(ctx, commit):
    """Generate a git commit message"""
    args = ctx.obj["args"]
    args.orders = common.DEFAULT_ORDERS
    args.orders.remove("openai")
    args.orders.insert(0, "openai")
    pprompt = prompt.GIT_COMMIT
    text = None
    if commit:
        args.no_clipboard_copy = True
        text = get_diff_from_staged_unstaged().strip()
    output = run.args(args, pprompt, text=text)
    if not output or output == "Veuillez fournir le texte à corriger.":
        if args.no_output:
            sys.exit(1)
        return
    if commit:
        git_commit(output)
    click.echo(output)
