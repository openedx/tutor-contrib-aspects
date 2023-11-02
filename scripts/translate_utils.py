import math
import os
import shutil
import yaml

ASSET_FOLDER_MAPPING = {
    "dashboard_title": "dashboards",
    "slice_name": "charts",
}


def get_text_for_translations(root_path):
    assets_path = (
        os.path.join(
            root_path,
            "tutoraspects/templates/aspects/build/aspects-superset/"
            "openedx-assets/assets/"
        )
    )

    print(f"Assets path: {assets_path}")

    strings = []

    for root, dirs, files in os.walk(assets_path):
        for file in files:
            if not file.endswith(".yaml"):
                continue

            path = os.path.join(root, file)
            with open(path, 'r') as asset_file:
                asset_str = asset_file.read()

            asset = yaml.safe_load(asset_str)
            strings.extend(mark_text_for_translation(asset))

    return strings


def mark_text_for_translation(asset):
    """
    For every asset extract the text and mark it for translation
    """

    def extract_text(asset, type):
        """
        Extract text from an asset
        """
        strings = []
        if type == "dashboards":
            strings.append(asset["dashboard_title"])

            # Gets translatable fields from filters
            for filter in asset["metadata"]["native_filter_configuration"]:
                strings.append(filter["name"])

            # Gets translatable fields from charts
            for element in asset.get("position", {}).values():
                if not isinstance(element, dict):
                    continue

                meta = element.get("meta", {})

                if meta.get("text"):
                    strings.append(meta["text"])

                if meta.get("code"):
                    strings.append(meta["code"])

        elif type == "charts":
            strings.append(asset["slice_name"])

            if asset.get("description"):
                strings.append(asset["description"])

            if asset["params"].get("x_axis_label"):
                strings.append(asset["params"]["x_axis_label"])

            if asset["params"].get("y_axis_label"):
                strings.append(asset["params"]["y_axis_label"])

        return strings

    for key, value in ASSET_FOLDER_MAPPING.items():
        if key in asset:
            strings = extract_text(asset, value)
            print(
                f"Extracted {len(strings)} strings from {value} {asset.get('uuid')}"
            )
            return strings

    # If we get here it's a type of asset that we don't translate, return nothing.
    return []


def compile_translations(root_path):
    """
    Combine translated files into the single file we use for translation.

    This should be called after we pull translations using Atlas, see the
    pull_translations make target.
    """
    translations_path = (
        os.path.join(
            root_path,
            "tutoraspects/templates/aspects/apps/superset/conf/locale"
        )
    )

    all_translations = {}
    for root, dirs, files in os.walk(translations_path):
        for file in files:
            if not file.endswith(".yaml"):
                continue

            lang = root.split(os.sep)[-1]
            path = os.path.join(root, file)
            with open(path, 'r') as asset_file:
                loc_str = asset_file.read()
            loaded_strings = yaml.safe_load(loc_str)

            # Sometimes translated files come back with "en" as the top level
            # key, but still translated correctly.
            try:
                all_translations[lang] = loaded_strings[lang]
            except KeyError:
                all_translations[lang] = loaded_strings["en"]

    out_path = (
        os.path.join(
            root_path,
            "tutoraspects/templates/aspects/apps/superset/localization/locale.yaml"
        )
    )

    print(f"Writing all translations out to {out_path}")
    with open(out_path, 'w') as outfile:
        outfile.write("---\n")
        # If we don't use an extremely large width, the jinja in our translations
        # can be broken by newlines. So we use the largest number there is.
        yaml.dump(all_translations, outfile, width=math.inf)
        outfile.write("\n{{ patch('superset-extra-asset-translations')}}\n")

    # We remove these files to avoid confusion about where translations are coming
    # from, and because otherwise we will need to re-save them with the large
    # width as above to avoid Jinja parsing errors.
    print("Removing downloaded translations files... ")
    shutil.rmtree(translations_path)


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
    STRINGS = set(get_text_for_translations(root_path))
    translations = {'en': {}}

    for string in STRINGS:
        translations['en'][string] = string

    print(f"Writing English strings to {translation_file}")
    with open(translation_file, "w") as file:
        file.write(yaml.dump(translations))

    print("Done compiling translations.")
