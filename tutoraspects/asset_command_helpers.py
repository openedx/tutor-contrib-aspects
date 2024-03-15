"""
Helpers for Tutor commands and "do" commands.
"""

from zipfile import ZipFile
import glob
import os
import re
import yaml

import click

FILE_NAME_ATTRIBUTE = "_file_name"

PLUGIN_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(
    PLUGIN_PATH,
    "templates",
    "aspects",
    "build",
    "aspects-superset",
    "openedx-assets",
    "assets",
)


def str_presenter(dumper, data):
    """
    Configures yaml for dumping multiline strings
    """
    if len(data.splitlines()) > 1 or "'" in data:  # check for multiline string
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, str_presenter)
yaml.representer.SafeRepresenter.add_representer(str, str_presenter)


class SupersetCommandError(Exception):
    """
    An error we can use for these methods.
    """


class Asset:
    """
    Base class for asset types used in import.
    """

    path = None
    assets_path = None
    templated_vars = None
    required_vars = None
    omitted_vars = None
    raw_vars = None

    def __init__(self):
        if not self.path:
            raise NotImplementedError("Asset is an abstract class.")

        self.assets_path = os.path.join(ASSETS_PATH, self.path)

    def get_path(self):
        """
        Returns the full path to the asset file type.
        """
        if self.assets_path:
            return self.assets_path
        raise NotImplementedError

    def get_templated_vars(self):
        """
        Returns a list of variables which should have templated variables.

        This allows us to alert users when they might be submitting hard coded
        values instead of something like {{ TABLE_NAME }}.
        """
        return self.templated_vars or []

    def get_required_vars(self):
        """
        Returns a list of variables which must exist for the asset.

        This allows us to make sure users remember to add `_roles` to dashboards.
        Since those do not export.
        """
        return self.required_vars or []

    def get_omitted_vars(self):
        """
        Returns a list of variables which should be omitted from the content.
        """
        return self.omitted_vars or []

    def get_raw_vars(self):
        """
        Returns a list of variables which should be omitted from the content.
        """
        return self.raw_vars or []

    def remove_content(self, content: dict):
        """
        Remove any variables from the content which should be omitted.
        """
        for var_path in self.get_omitted_vars():
            self._remove_content(content, var_path.split("."))

    def _remove_content(self, content: dict, var_path: list):
        """
        Helper method to remove content from the content dict.
        """
        if content is None:
            return
        if len(var_path) == 1:
            content.pop(var_path[0], None)
            return
        if var_path[0] in content:
            self._remove_content(content[var_path[0]], var_path[1:])

    def omit_templated_vars(self, content: dict, existing: dict):
        """
        Omit templated variables from the content if they are not present in
        the existing file content.
        """
        if not existing:
            return

        for key in content.keys():
            if key not in existing.keys():
                continue
            if isinstance(existing[key], str):
                if "{{" in existing.get(key, "") or "{%" in existing.get(key, ""):
                    if key in self.get_raw_vars():
                        raw_expression = "{% raw %}" + content[key] + "{% endraw %}"
                        content[key] = raw_expression
                    else:
                        content[key] = existing[key]

            if isinstance(existing[key], dict):
                self.omit_templated_vars(content[key], existing[key])

            if isinstance(existing[key], list):
                for i, item in enumerate(content[key]):
                    if isinstance(item, dict):
                        try:
                            tmp = existing[key][i]
                            self.omit_templated_vars(item, tmp or None)
                        except IndexError:
                            pass


class ChartAsset(Asset):
    """
    Chart assets.
    """

    path = "charts"
    omitted_vars = [
        "params.dashboards",
        "params.datasource",
        "params.slice_id",
    ]
    raw_vars = ["sqlExpression", "query_context"]


class DashboardAsset(Asset):
    """
    Dashboard assets.
    """

    path = "dashboards"
    required_vars = ["_roles"]


class DatasetAsset(Asset):
    """
    Dataset assets.
    """

    path = "datasets"
    templated_vars = ["schema", "table_name", "sql"]
    omitted_vars = ["extra.certification"]


class DatabaseAsset(Asset):
    """
    Database assets.
    """

    path = "databases"
    templated_vars = ["sqlalchemy_uri"]


ASSET_TYPE_MAP = {
    "slice_name": ChartAsset(),
    "dashboard_title": DashboardAsset(),
    "table_name": DatasetAsset(),
    "database_name": DatabaseAsset(),
}


def validate_asset_file(asset_path, content, echo):
    """
    Check various aspects of the asset file based on its type.

    Returns the destination path for the file to import to.
    """
    orig_filename = os.path.basename(asset_path)
    out_filename = re.sub(r"(_\d*)\.yaml", ".yaml", orig_filename)
    content[FILE_NAME_ATTRIBUTE] = out_filename

    out_path = None
    needs_review = False
    for key, cls in ASSET_TYPE_MAP.items():
        if key in content:
            out_path = cls.get_path()

            existing = None

            # Check if the file already exists
            if os.path.exists(os.path.join(out_path, out_filename)):
                with open(
                    os.path.join(out_path, out_filename), encoding="utf-8"
                ) as stream:
                    existing = yaml.safe_load(stream)

            for var in cls.get_templated_vars():
                # If this is a variable we expect to be templated,
                # check that it is.
                if (
                    content[var]
                    and not content[var].startswith("{{")
                    and not content[var].startswith("{%")
                ):
                    if existing:
                        content[var] = existing[var]
                        needs_review = False
                    else:
                        echo(
                            click.style(
                                f"WARN: {orig_filename} has "
                                f"{var} set to {content[var]} instead of a "
                                f"setting.",
                                fg="yellow",
                            )
                        )
                        needs_review = True

            for var in cls.get_required_vars():
                # If this variable is required and doesn't exist, warn.
                if var not in content:
                    if existing:
                        content[var] = existing[var]
                        needs_review = False
                    else:
                        echo(
                            click.style(
                                f"WARN: {orig_filename} is missing required "
                                f"item '{var}'!",
                                fg="red",
                            )
                        )
                        needs_review = True

            cls.remove_content(content)
            cls.omit_templated_vars(content, existing)
            # We found the correct class, we can stop looking.
            break
    return out_path, needs_review


def import_superset_assets(file, echo):
    """
    Import assets from a Superset export zip file to the openedx-assets directory.
    """
    written_assets = []
    review_files = set()
    err = 0

    with ZipFile(file.name) as zip_file:
        for asset_path in zip_file.namelist():
            if "metadata.yaml" in asset_path:
                continue
            with zip_file.open(asset_path) as asset_file:
                content = yaml.safe_load(asset_file)
                out_path, needs_review = validate_asset_file(asset_path, content, echo)

                # This can happen if it's an unknown asset type
                if not out_path:
                    continue

                if needs_review:
                    review_files.add(content[FILE_NAME_ATTRIBUTE])

                out_path = os.path.join(out_path, content[FILE_NAME_ATTRIBUTE])
                written_assets.append(out_path)

                with open(out_path, "w", encoding="utf-8") as out_f:
                    yaml.dump(content, out_f, encoding="utf-8")

    if review_files:
        echo()
        echo(
            click.style(
                f"{len(review_files)} files had warnings and need review:", fg="red"
            )
        )
        for filename in review_files:
            echo(f"    - {filename}")

        raise SupersetCommandError(
            "Warnings found, please review then run "
            "'tutor aspects check_superset_assets'"
        )

    echo()
    echo(f"Serialized {len(written_assets)} assets")

    return err


def _get_asset_files():
    for file_name in glob.iglob(ASSETS_PATH + "/**/*.yaml", recursive=True):
        with open(file_name, "r", encoding="utf-8") as file:
            # We have to remove the jinja for it to parse
            file_str = file.read()
            file_str = file_str.replace("{{", "").replace("}}", "")
            asset = yaml.safe_load(file_str)

            # Some asset types are lists of one element for some reason
            if isinstance(asset, list):
                asset = asset[0]

            yield file_name, asset


def _deduplicate_asset_files(existing, found, echo):
    if existing["modified"] == found["modified"]:
        short_existing = os.path.basename(existing["file_name"])
        short_found = os.path.basename(found["file_name"])
        raise SupersetCommandError(
            "Modified dates are identical. You will need to  "
            f"remove either {short_existing} or "
            f" {short_found} and run again."
        )

    newer_file = existing if existing["modified"] > found["modified"] else found
    old_file = existing if existing["modified"] < found["modified"] else found

    short_new = os.path.basename(newer_file["file_name"])
    short_old = os.path.basename(old_file["file_name"])

    echo(f"{short_new} is newer, {short_old} will be deleted")

    os.remove(old_file["file_name"])

    return newer_file


def deduplicate_superset_assets(echo):
    """
    Check for duplicated UUIDs in openedx-assets, delete the older file.

    Superset exports use the name of the asset in the filename, so if you
    rename a chart or dashboard a new file will be created with the same
    UUID, causing import issues. This tries to fix that.
    """
    echo("De-duplicating assets...")
    err = 0
    uuid_file_map = {}

    for file_name, asset in _get_asset_files():
        curr_uuid = asset["uuid"]
        if curr_uuid in uuid_file_map:
            echo()
            echo(
                click.style(f"WARN: Duplicate UUID found {asset['uuid']}", fg="yellow")
            )

            new_file = {"file_name": file_name, "modified": os.stat(file_name)[8]}
            old_file = uuid_file_map[curr_uuid]

            try:
                uuid_file_map[curr_uuid] = _deduplicate_asset_files(
                    old_file, new_file, echo
                )
            except SupersetCommandError as ex:
                echo(click.style(f"ERROR: {ex}", fg="red"))
                err += 1
                continue
        else:
            uuid_file_map[asset["uuid"]] = {
                "file_name": file_name,
                "modified": os.stat(file_name)[8],
            }

    if err:
        echo()
        echo()
        echo(click.style(f"{err} errors found!", fg="red"))

    echo("Deduplication complete.")


def check_asset_names(echo):
    """
    Warn about any duplicate asset names.
    """
    echo("Looking for duplicate names...")
    warn = 0

    names = set()
    for file_name, asset in _get_asset_files():
        for k in ("slice_name", "dashboard_title", "database_name"):
            if k in asset:
                if asset[k] in names:
                    warn += 1
                    echo(
                        f"WARNING: Duplicate name {asset[k]} in {file_name}, this "
                        f"could confuse users, consider changing it."
                    )
                names.add(asset[k])
                break

    echo(f"{warn} duplicate names detected.")
