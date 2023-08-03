import os
import sys

import click
from transifex.native import init
from utils import (LANGUAGES, compile_translations, get_text_for_translations,
                   push_translations)

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
    elif action == "list":
        get_text_for_translations(root)
    else:
        print("Unknown action: {}".format(action))
        sys.exit(1)


if __name__ == "__main__":
    command()
