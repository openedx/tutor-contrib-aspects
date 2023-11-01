import os
import sys

import click
from translate_utils import compile_translations, extract_translations, get_text_for_translations


@click.command()
@click.argument("root")
@click.argument("action")
def command(root, action):
    """Interface for the translations."""
    if action == "extract":
        extract_translations(root)
    elif action == "compile":
        compile_translations(root)
    elif action == "list":
        get_text_for_translations(root)
    else:
        print("Unknown action: {}".format(action))
        sys.exit(1)


if __name__ == "__main__":
    command()
