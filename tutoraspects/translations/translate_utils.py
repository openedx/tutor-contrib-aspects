"""Translations utilities for Tutor Aspects."""

import os
import glob

import ruamel.yaml
import ruamel.yaml.comments

from tutoraspects.utils import recursive_sort_mappings, yaml


class TranslatableAsset:
    """A class to represent an asset that can be translated."""

    translatable_attributes = []

    def __init__(self, asset: dict):
        self.asset = asset
        for key, value in ASSET_FOLDER_MAPPING.items():
            if key in asset:
                self.asset_type = value
                break

    def extract_text(self):
        """
        Extract text from an asset.
        """
        strings = []
        for var_path in self.translatable_attributes:
            current_strings = self.translate_var(self.asset, var_path.split("."))
            if None in current_strings:
                print(
                    f"\tFound None in {var_path} for {self.asset_type[0]} {self.asset.get('uuid')}"
                )
            strings.extend(current_strings)

        return list(filter(lambda a: a is not None, strings))

    def translate_var(
        self, content, var_path
    ):  # pylint: disable=too-many-return-statements
        """
        Helper method to remove content from the content dict.
        """
        if not content or isinstance(content, str):
            return []

        # if content is a list, run method for each list item
        if isinstance(content, list):
            strings = []
            for item in content:
                strings.extend(self.translate_var(item, var_path))
            return strings

        if isinstance(content, dict):
            # if var_path is wild, run method on every value in dict
            if var_path[0] == "*":
                strings = []
                for value in content.values():
                    strings.extend(self.translate_var(value, var_path[1:]))
                return strings
            # if there is only 1 value in var_path, find it in the dict
            if len(var_path) == 1:
                strings = []
                result = content.get(var_path[0])
                if result:
                    strings.append(result)
                return strings
            # otherwise, run method again 1 level deeper
            return self.translate_var(content.get(var_path[0], " "), var_path[1:])

        print("Could not translate var_path: ", var_path, content)
        return []


class DashboardAsset(TranslatableAsset):
    """A class to represent a dashboard that can be translated."""

    translatable_attributes = [
        "dashboard_title",
        "description",
        "metadata.native_filter_configuration.name",
        "metadata.native_filter_configuration.description",
        "position.*.meta.text",
        "position.*.meta.code",
        "position.*.meta.sliceNameOverride",
    ]


class ChartAsset(TranslatableAsset):
    """A class to represent a chart that can be translated."""

    translatable_attributes = [
        "slice_name",
        "description",
        "params.x_axis_label",
        "params.y_axis_label",
        "params.groupby.label",
    ]


class DatasetAsset(TranslatableAsset):
    """A class to represent a dataset that can be translated."""

    translatable_attributes = [
        "metrics.verbose_name",
        "columns.verbose_name",
    ]


ASSET_FOLDER_MAPPING = {
    "dashboard_title": ("dashboards", DashboardAsset),
    "slice_name": ("charts", ChartAsset),
    "table_name": ("datasets", DatasetAsset),
}

BASE_PATH = "tutoraspects/templates/aspects/build/aspects-superset/"


def get_text_for_translations(root_path):
    """
    Extract all translatable text from the Superset assets.
    """
    assets_path = os.path.join(root_path, BASE_PATH, "openedx-assets/assets/")
    print(f"Assets path: {assets_path}")

    strings = []

    yaml_files = glob.glob(os.path.join(assets_path, "**/*.yaml"))

    for yaml_file in yaml_files:
        with open(yaml_file, "r", encoding="utf-8") as asset_file:
            asset_str = asset_file.read()

        asset = yaml.load(asset_str)
        strings.extend(mark_text_for_translation(asset))

    with open(
        BASE_PATH + "localization/datasets_strings.yaml", "r", encoding="utf-8"
    ) as file:
        dataset_strings = yaml.load(file.read())
        for key in dataset_strings:
            strings.extend(dataset_strings[key])
            print(f"Extracted {len(dataset_strings[key])} strings for dataset {key}")
    return strings


def mark_text_for_translation(asset):
    """
    For every asset extract the text and mark it for translation
    """

    for key, (asset_type, Asset) in ASSET_FOLDER_MAPPING.items():
        if key in asset:
            strings = Asset(asset).extract_text()
            print(
                f"Extracted {len(strings)} strings from {asset_type} {asset.get('uuid')}"
            )
            return strings

    # If we get here it's a type of asset that we don't translate, return nothing.
    return []


def extract_translations(root_path):
    """
    This gathers all translatable text from the Superset assets.

    An English locale file is created, which openedx-translations will send to
    Transifex for translation.
    """
    # The expectation is that this will end up at the site root, which should
    # be cwd for make targets. This is a temporary file used only in the Github
    # action in openedx-translations.
    translation_file = "transifex_input.yaml"

    print("Gathering text for translations...")
    strings = set(get_text_for_translations(root_path))
    print(f"Extracted {len(strings)} strings for translation.")
    translations = ruamel.yaml.comments.CommentedMap()
    translations["en"] = ruamel.yaml.comments.CommentedMap()

    for string in strings:
        translations["en"][string] = string

    print(f"Writing English strings to {translation_file}")
    with open(translation_file, "w", encoding="utf-8") as file:
        recursive_sort_mappings(translations)
        yaml.dump(translations, file)

    print("Done compiling translations.")
