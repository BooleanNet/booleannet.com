"""bnet command line."""

import click

from booleannet.commands.gviz import cli as gviz
from booleannet.commands.models import main as models

try:
    import pyboolnet
except ImportError:
    print("# Error: pyboolnet is not installed. See the docs`.")
    exit(1)

# Subcommand name -> click command. Add a new tool here.
COMMANDS = {
    "models": models,
    "graphviz": gviz,
}


@click.group("bnet", no_args_is_help=True)
def main() -> None:
    """BooleanNet command line tools."""


for name, cmd in COMMANDS.items():
    main.add_command(cmd, name=name)
