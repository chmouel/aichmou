#!/usr/bin/env python
# Author: Chmouel Boudjnah <chmouel@chmouel.com>

import click

import aichmou.args
import aichmou.commands  # noqa


def main():
    click.echo(aichmou.args.cli())


if __name__ == "__main__":
    main()
