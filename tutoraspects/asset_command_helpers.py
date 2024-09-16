"""
Helpers for Tutor commands and "do" commands.
"""

import glob
import os
import re
import json
from zipfile import ZipFile
from sqlfmt.api import format_string
from sqlfmt.mode import Mode

import click
import yaml

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
    for _, asset in _get_asset_files():
        for k in ("slice_name", "dashboard_title", "database_name"):
            if k in asset:
                if asset[k] in names:
                    warn += 1
                    echo(
                        f"WARNING: Duplicate {k} {asset[k]} in {asset.get('_file_name')}"
                    )
                names.add(asset[k])
                break

    echo(
        f"{warn} duplicate names detected. This could confuse users, consider changing them."
    )


def _get_all_chart_dataset_uuids():
    """
    Return the UUIDs of all datasets and charts in our file assets.
    """
    all_dataset_uuids = {}
    all_chart_uuids = {}

    # First get all known uuid's
    for file_path, asset in _get_asset_files():
        if "slice_name" in asset:
            all_chart_uuids[asset["uuid"]] = {
                "name": asset["_file_name"],
                "file_path": file_path,
            }
        elif "table_name" in asset:
            all_dataset_uuids[asset["uuid"]] = {
                "name": asset["table_name"],
                "file_path": file_path,
            }

    return all_dataset_uuids, all_chart_uuids


def _get_used_chart_dataset_uuids():
    """
    Return the UUIDs of all datasets and charts actually used in our file assets.
    """
    used_dataset_uuids = set()
    used_chart_uuids = set()

    for _, asset in _get_asset_files():
        if "dashboard_title" in asset:
            filters = asset["metadata"].get("native_filter_configuration", [])

            for filter_config in filters:
                for item in filter_config.get("targets", {}):
                    if item.get("datasetUuid"):
                        used_dataset_uuids.add(item.get("datasetUuid"))

            for pos in asset["position"]:
                if pos.startswith("CHART-"):
                    slice_uuid = asset["position"][pos]["meta"].get("uuid")

                    if slice_uuid:
                        used_chart_uuids.add(slice_uuid)

        if "slice_name" in asset:
            dataset_uuid = asset["dataset_uuid"]
            used_dataset_uuids.add(dataset_uuid)

    return used_dataset_uuids, used_chart_uuids


def _find_orphan_assets(echo):
    """
    Find potentially unused assets.
    UUIDs listed as 'ignored' in aspects_asset_list.yaml are owned
    by Aspects and will be removed from the list of potential orphans.
    """
    all_dataset_uuids, all_chart_uuids = _get_all_chart_dataset_uuids()
    used_dataset_uuids, used_chart_uuids = _get_used_chart_dataset_uuids()

    # Remove uuids from all list that are in used list
    for k in used_dataset_uuids:
        try:
            all_dataset_uuids.pop(k)
        except KeyError:
            echo(click.style(f"WARNING: Dataset {k} used but not found!", fg="red"))

    for k in used_chart_uuids:
        try:
            all_chart_uuids.pop(k)
        except KeyError:
            echo(click.style(f"WARNING: Chart {k} used but not found!", fg="red"))

    # Remove uuids from all list that are in ignored yaml
    with open(os.path.join(PLUGIN_PATH, "aspects_asset_list.yaml"), "r", encoding="utf-8") as file:
        aspects_assets = yaml.safe_load_all(file)

        for line in aspects_assets:
            ignored_uuids = line.get("ignored_uuids")
            if ignored_uuids and ignored_uuids.get("datasets"):
                for k in ignored_uuids.get("datasets"):
                    all_dataset_uuids.pop(k, None)

            if ignored_uuids and ignored_uuids.get("charts"):
                for k in ignored_uuids.get("charts"):
                    all_chart_uuids.pop(k, None)

    if not all_dataset_uuids and not all_chart_uuids:
        echo(f"{len(all_chart_uuids) + len(all_dataset_uuids)} orphans detected.")

    return all_dataset_uuids, all_chart_uuids


def check_orphan_assets(echo):
    """
    Warn about any potentially unused assets.
    """
    echo("Looking for potentially orphaned assets...")
    echo()

    all_dataset_uuids, all_chart_uuids = _find_orphan_assets(echo)

    if all_dataset_uuids:
        echo(click.style("Potentially unused datasets detected:", fg="yellow"))
        echo("Add the UUIDs to aspects_asset_list.yaml to be deleted")
        for x, y in all_dataset_uuids.items():
            echo(f'{y.get("name")} (UUID: {x})')

    if all_chart_uuids:
        echo(click.style("Potentially unused charts detected:", fg="yellow"))
        echo("Add the UUIDs to aspects_asset_list.yaml to be deleted")
        for x, y in all_chart_uuids.items():
            echo(f'{y.get("name")} (UUID: {x})')


def delete_aspects_orphan_assets(echo):
    """
    Delete any unused charts and datasets whose UUIDs are listed in
    aspects_assets_list.yaml - these are owned by Aspects and can safely
    be deleted.
    """
    unused_dataset_uuids, unused_chart_uuids = _find_orphan_assets(echo)

    with open(os.path.join(PLUGIN_PATH, "aspects_asset_list.yaml"), "r") as file:
        aspects_assets = yaml.safe_load_all(file)

        delete_count = 0
        for line in aspects_assets:
            orphaned_uuids = line.get("orphaned_uuids")
            for uuid, data in unused_dataset_uuids.items():
                if orphaned_uuids and orphaned_uuids.get("datasets"):
                    if uuid in orphaned_uuids.get("datasets"):
                        echo(
                            f"Deleting orphan dataset {data.get('name')} (UUID: {uuid})"
                        )
                        os.remove(data.get("file_path"))
                        delete_count += 1

            for uuid, data in unused_chart_uuids.items():
                if orphaned_uuids and orphaned_uuids.get("charts"):
                    if uuid in orphaned_uuids.get("charts"):
                        echo(
                            f"Deleting orphan chart {data.get('name')} (UUID: {uuid})"
                        )
                        os.remove(data.get("file_path"))
                        delete_count += 1

    echo(f"Deleted {delete_count} assets")
