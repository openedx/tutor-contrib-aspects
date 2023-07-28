import os
import sys

import click
import yaml
from transifex.native import init, tx
from transifex.native.parsing import SourceString
from utils import LANGUAGES, compile_translations, push_translations

init(
    os.getenv("TRANSIFEX_TOKEN"),
    LANGUAGES,
    os.getenv("TRANSIFEX_SECRET"),
)


@click.command()
@click.argument("root")
@click.argument("action")
def command(root, action):
    """Interface for the translations."""
    if action == "push":
        push_translations(root)
    elif action == "compile":
        compile_translations(root)
    else:
        print("Unknown action: {}".format(action))
        sys.exit(1)


if __name__ == "__main__":
    command()
