import yaml
from transifex.native import tx
from transifex.native.parsing import SourceString

ASSET_FOLDER_MAPPING = {
    "dashboard_title": "dashboards",
    "slice_name": "charts",
    "database_name": "databases",
    "table_name": "datasets",
}

LANGUAGES = [
    "es",
    "it",
    "fr",
    "zh",
    "ja",
    "de",
    "pt",
    "ru",
    "ko",
    "sk",
    "sl",
    "nl",
]


def get_text_for_translations(root_path):
    assets_file = (
        root_path + "/env/plugins/aspects/apps/superset/pythonpath/assets.yaml"
    )

    strings = []

    file = yaml.load(open(assets_file, "r"), Loader=yaml.FullLoader)

    for asset in file:
        strings.extend(mark_text_for_translation(asset))

    return strings


def mark_text_for_translation(asset):
    """For every asset extract the text and mark it for translation"""

    def extract_text(asset, type):
        """Extract text from an asset"""
        strings = []
        if type == "dashboards":
            strings.append(asset["dashboard_title"])

            for element in asset.get("position", {}).values():
                if not isinstance(element, dict):
                    continue

                meta = element.get("meta", {})

                if element.get("type") == "TAB" and meta.get("text"):
                    strings.append(meta["text"])

        elif type == "charts":
            strings.append(asset["slice_name"])
        elif type == "databases":
            # WARNING: Databases are not translated
            pass
        elif type == "datasets":
            # WARNING: Datasets are not translated
            pass
        return strings

    for key, value in ASSET_FOLDER_MAPPING.items():
        if key in asset:
            strings = extract_text(asset, value)
            print(
                f"Extracting text from {value} {asset.get('uuid')}",
                strings,
            )
            return strings


def compile_translations(root_path):
    print("Fetching translations...")
    tx.fetch_translations()

    translation_file = (
        "tutoraspects/templates/aspects/apps/superset/pythonpath/locale.yaml"
    )
    file = open(translation_file, "w")

    STRINGS = get_text_for_translations(root_path)

    translations = {}

    print("Compiling translations...")

    for language in LANGUAGES:
        print("Processing language", language)
        translations[language] = {}
        for string in STRINGS:
            if not translations[language].get(string):
                translation = tx.get_translation(string, language, None)
                translations[language][string] = translation if translation else ""

    file.write(yaml.dump(translations))

    file.write("{{ patch('superset-extra-asset-translations')}}\n")


def push_translations(root_path):
    print("Publishing translation strings...")

    STRINGS = get_text_for_translations(root_path)

    source_strings = []
    for text in STRINGS:
        source_string = SourceString(
            text,
        )
        source_strings.append(source_string)

    response_code, response_content = tx.push_source_strings(source_strings, purge=True)
    print(response_code, response_content)
