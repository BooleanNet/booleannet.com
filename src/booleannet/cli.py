"""bnet command line."""

import importlib
import pkgutil

import click

from booleannet import commands


@click.group("bnet", no_args_is_help=True)
def main() -> None:
    """BooleanNet command line tools."""


def load_commands() -> None:
    """Register each commands module that defines a click command named cli.

    The module filename is the subcommand: commands/dot.py becomes ``bnet dot``.
    """
    prefix = commands.__name__ + "."
    for info in pkgutil.iter_modules(commands.__path__, prefix):
        mod = importlib.import_module(info.name)
        cmd = getattr(mod, "cli", None)
        if isinstance(cmd, click.Command):
            main.add_command(cmd, name=info.name.removeprefix(prefix))


load_commands()
