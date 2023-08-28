"""Import a list of assets from a yaml file and create them in the superset assets folder."""
import os
import uuid
from zipfile import ZipFile

import yaml
from superset.app import create_app

app = create_app()
app.app_context().push()

from copy import deepcopy

from superset import security_manager
from superset.commands.importers.v1.assets import ImportAssetsCommand
from superset.commands.importers.v1.utils import get_contents_from_bundle
from superset.extensions import db
from superset.models.dashboard import Dashboard
from superset.utils.database import get_or_create_db

BASE_DIR = "/app/assets/superset"

ASSET_FOLDER_MAPPING = {
    "dashboard_title": "dashboards",
    "slice_name": "charts",
    "database_name": "databases",
    "table_name": "datasets",
}

ENABLED_LANGUAGES = {{SUPERSET_SUPPORTED_LANGUAGES}}

for folder in ASSET_FOLDER_MAPPING.values():
    os.makedirs(f"{BASE_DIR}/{folder}", exist_ok=True)

FILE_NAME_ATTRIBUTE = "_file_name"

TRANSLATIONS_FILE_PATH = "/app/pythonpath/locale.yaml"
ASSETS_FILE_PATH = "/app/pythonpath/assets.yaml"
ASSETS_ZIP_PATH = "/app/assets/assets.zip"

merged_data = {}
with open(TRANSLATIONS_FILE_PATH, "r") as file:
    yaml_content = file.read()
    yaml_documents = yaml_content.split("\n---\n")

    for doc in yaml_documents:
        data = yaml.safe_load(doc)
        if data is not None:
            for lang, translations in data.items():
                if lang not in merged_data:
                    merged_data[lang] = {}
                merged_data[lang].update(translations)


ASSETS_TRANSLATIONS = merged_data


def main():
    create_assets()


def create_assets():
    """Create assets from a yaml file."""
    roles = {}
    with open(ASSETS_FILE_PATH, "r") as file:
        extra_assets = yaml.safe_load(file)

        if not extra_assets:
            print("No extra assets to create")
            return

        # For each asset, create a file in the right folder
        for asset in extra_assets:
            if FILE_NAME_ATTRIBUTE not in asset:
                raise Exception(f"Asset {asset} has no {FILE_NAME_ATTRIBUTE}")
            file_name = asset.pop(FILE_NAME_ATTRIBUTE)

            # Find the right folder to create the asset in
            for asset_name, folder in ASSET_FOLDER_MAPPING.items():
                if not asset_name in asset:
                    continue

                write_asset_to_file(asset, asset_name, folder, file_name, roles)
                break

    create_zip_and_import_assets()
    update_dashboard_roles(roles)


def get_uuid5(base_uuid, name):
    """Generate an idempotent uuid."""
    base_uuid = uuid.UUID(base_uuid)
    base_namespace = uuid.uuid5(base_uuid, "superset")
    return uuid.uuid5(base_namespace, name)


def write_asset_to_file(asset, asset_name, folder, file_name, roles):
    """Write an asset to a file and generated translated assets"""
    if folder == "databases":
        # This will fix the URI connection string by setting the right password.
        create_superset_db(asset["database_name"], asset["sqlalchemy_uri"])

    if folder in ["charts", "dashboards"]:
        for language in ENABLED_LANGUAGES.keys():
            updated_asset = generate_translated_asset(
                asset, asset_name, folder, language, roles
            )

            path = f"{BASE_DIR}/{folder}/{file_name}-{language}.yaml"
            with open(path, "w") as file:
                yaml.dump(updated_asset, file)

    ## WARNING: Dashboard are assigned a Dummy role which prevents users to
    #           access the original dashboards.
    dashboard_roles = asset.pop("_roles", None)
    if dashboard_roles:
        roles[asset["uuid"]] = [security_manager.find_role("Admin")]

    path = f"{BASE_DIR}/{folder}/{file_name}.yaml"
    with open(path, "w") as file:
        yaml.dump(asset, file)


def generate_translated_asset(asset, asset_name, folder, language, roles):
    """Generate a translated asset with their elements updated"""
    copy = deepcopy(asset)
    copy["uuid"] = str(get_uuid5(copy["uuid"], language))
    copy[asset_name] = get_translation(copy[asset_name], language)

    if folder == "dashboards":
        copy["slug"] = f"{copy['slug']}-{language}"

        dashboard_roles = copy.pop("_roles", [])
        translated_dashboard_roles = []

        for role in dashboard_roles:
            translated_dashboard_roles.append(f"{role} - {language}")

        roles[copy["uuid"]] = [
            security_manager.find_role(role) for role in translated_dashboard_roles
        ]

        generate_translated_dashboard_elements(copy, language)
        generate_translated_dashboard_filters(copy, language)
    return copy


def generate_translated_dashboard_elements(copy, language):
    """Generate translated elements for a dashboard"""
    position = copy.get("position", {})

    SUPPORTED_TYPES = {"TAB": "text", "HEADER": "text", "MARKDOWN": "code"}

    for element in position.values():
        if not isinstance(element, dict):
            continue

        meta = element.get("meta", {})
        original_uuid = meta.get("uuid", None)

        element_type = element.get("type", "Unknown")

        translation, element_type, element_id = None, None, None

        if original_uuid:
            element_type = "Chart"
            element_id = str(get_uuid5(original_uuid, language))
            translation = get_translation(meta["sliceName"], language)

            meta["sliceName"] = translation
            meta["uuid"] = element_id

        elif element.get("type") in SUPPORTED_TYPES.keys():
            text_key = SUPPORTED_TYPES.get(element["type"])
            chart_body_id = element.get("id")
            if not meta or not meta.get(text_key):
                continue

            element_type = element.get("type")
            element_id = chart_body_id
            translation = get_translation(meta[text_key], language)

            meta[text_key] = translation

        if translation and element_type and element_id:
            print(
                f"Generating {element_type} {element_id} for language {language} {translation}"
            )


def generate_translated_dashboard_filters(copy, language):
    """Generate translated filters for a dashboard"""
    metadata = copy.get("metadata", {})

    for filter in metadata.get("native_filter_configuration", []):
        element_type = "Filter"
        element_id = filter["id"]
        translation = get_translation(filter["name"], language)

        filter["name"] = translation
        print(
            f"Generating {element_type} {element_id} for language {language} {translation}"
        )


def create_superset_db(database_name, uri) -> None:
    """Create a database object with the right URI"""
    superset_db = get_or_create_db(database_name, uri, always_create=True)
    db.session.add(superset_db)
    db.session.commit()


def create_zip_and_import_assets():
    """Create a zip file with all the assets and import them in superset"""
    with ZipFile(ASSETS_ZIP_PATH, "w") as zip:
        for folder in ASSET_FOLDER_MAPPING.values():
            for file_name in os.listdir(f"{BASE_DIR}/{folder}"):
                zip.write(
                    f"{BASE_DIR}/{folder}/{file_name}", f"import/{folder}/{file_name}"
                )
        zip.write(f"{BASE_DIR}/metadata.yaml", "import/metadata.yaml")
        contents = get_contents_from_bundle(zip)
        command = ImportAssetsCommand(contents)
        command.run()

    os.remove(ASSETS_ZIP_PATH)


def update_dashboard_roles(roles):
    """Update the roles of the dashboards"""
    owners_username = {{SUPERSET_OWNERS}}

    owners = []

    for owner in owners_username:
        user = security_manager.find_user(username=owner)
        if user:
            owners.append(user)

    for dashboard_uuid, role_ids in roles.items():
        dashboard = db.session.query(Dashboard).filter_by(uuid=dashboard_uuid).one()
        print("Importing dashboard roles", dashboard_uuid, role_ids)
        dashboard.roles = role_ids
        dashboard.published = True
        if owners:
            dashboard.owners = owners
        db.session.commit()


def get_translation(text, language):
    """Get a translation for a text in a language"""
    default_text = f"{text} - {language}"
    LANGUAGE = ASSETS_TRANSLATIONS.get(language, {})
    if not LANGUAGE:
        return default_text
    return ASSETS_TRANSLATIONS.get(language, {}).get(text) or default_text


if __name__ == "__main__":
    main()
