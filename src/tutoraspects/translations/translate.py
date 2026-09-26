"""Interface for the translations."""

import os
import site
import sys

import click

# Ensure that our whole source tree is on the path, otherwise actions in
# openedx-translations will fail.
site.addsitedir(os.path.join(os.path.dirname(__file__), "../.."))

# pylint: disable=wrong-import-position
from tutoraspects.translations.translate_utils import (
    extract_translations,
    get_text_for_translations,
)


@click.command()
@click.argument("root")
@click.argument("action")
def command(root, action):
    """Interface for the translations."""
    if action == "extract":
        extract_translations(root)
    elif action == "list":
        get_text_for_translations(root)
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)


if __name__ == "__main__":
    command()  # pylint: disable=no-value-for-parameter
