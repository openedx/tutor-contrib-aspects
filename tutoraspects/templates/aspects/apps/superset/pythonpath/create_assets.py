"""Import a list of assets from a yaml file and create them in the superset assets folder."""
import os
import uuid
import yaml
from zipfile import ZipFile
from superset.app import create_app

app = create_app()
app.app_context().push()

from superset import security_manager
from superset.commands.importers.v1.assets import ImportAssetsCommand
from superset.commands.importers.v1.utils import get_contents_from_bundle
from superset.extensions import db
from superset.models.dashboard import Dashboard
from superset.utils.database import get_or_create_db

from copy import deepcopy

BASE_DIR = "/app/assets/superset"

ASSET_FOLDER_MAPPING = {
    "dashboard_title": "dashboards",
    "slice_name": "charts",
    "database_name": "databases",
    "table_name": "datasets",
}

for folder in ASSET_FOLDER_MAPPING.values():
    os.makedirs(f"{BASE_DIR}/{folder}", exist_ok=True)

FILE_NAME_ATTRIBUTE = "_file_name"

TRANSLATIONS_FILE_PATH = "/app/pythonpath/locale.yaml"
ASSETS_FILE_PATH = "/app/pythonpath/assets.yaml"
ZIP_PATH = "/app/assets/assets.zip"

TRANSLATIONS = yaml.load(open(TRANSLATIONS_FILE_PATH, "r"), Loader=yaml.FullLoader)

print("\n\n TRANSLATIONS \n\n")

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

                write_asset_to_file(asset, folder, file_name, roles)
                break

    create_zip_and_import_assets()
    update_dashboard_roles(roles)


def get_uuid5(base_uuid, name):
    """Generate an idempotent uuid."""
    base_uuid = uuid.UUID(base_uuid)
    base_namespace = uuid.uuid5(base_uuid, "superset")
    return uuid.uuid5(base_namespace, name)


def write_asset_to_file(asset, folder, file_name, roles):
    if folder == "databases":
        # This will fix the URI connection string by setting the right password.
        create_superset_db(asset["database_name"], asset["sqlalchemy_uri"])

    asset_translation = TRANSLATIONS.get(asset.get("uuid"), {})

    for language, title in asset_translation.items():
        updated_asset = generate_asset(asset, folder, language, title, roles)

        path = f"{BASE_DIR}/{folder}/{file_name}-{language}.yaml"
        with open(path, "w") as file:
            yaml.dump(updated_asset, file)

    dashboard_roles = asset.pop("_roles", None)
    if dashboard_roles:
        roles[asset["uuid"]] = [
            security_manager.find_role(role) for role in dashboard_roles
        ]

    path = f"{BASE_DIR}/{folder}/{file_name}.yaml"
    with open(path, "w") as file:
        yaml.dump(asset, file)


def generate_asset(asset, folder, language, title, roles):
    copy = deepcopy(asset)
    copy["uuid"] = str(get_uuid5(copy["uuid"], language))
    if folder == "dashboards":
        copy["dashboard_title"] = title
        copy["slug"] = f"{copy['slug']}-{language}"

        dashboard_roles = copy.pop("_roles", None)
        translated_dashboard_roles = []

        for role in dashboard_roles:
            translated_dashboard_roles.append(f"{role} - {language}")

        roles[copy["uuid"]] = [
            security_manager.find_role(role) for role in translated_dashboard_roles
        ]
        position = copy.get("position", {})

        for chart_body in position.values():
            if not type(chart_body) == dict:
                continue
            if chart_body.get("meta") and chart_body["meta"].get("uuid"):
                if not chart_body["meta"].get("uuid") in TRANSLATIONS:
                    print(
                        f"Chart {chart_body['meta']['uuid']} not found in translations"
                    )
                    continue
                original_uuid = chart_body["meta"]["uuid"]
                chart_body["meta"]["uuid"] = str(get_uuid5(original_uuid, language))
                chart_body["meta"]["sliceName"] = TRANSLATIONS[original_uuid][language]
                print(
                    f"Generating chart {chart_body['meta']['uuid']} for {language} {chart_body['meta']['sliceName']}"
                )
    elif folder == "charts":
        copy["slice_name"] = title
    elif folder == "datasets":
        copy["table_name"] = title
    elif folder == "databases":
        copy["database_name"] = title
    return copy


def create_superset_db(database_name, uri) -> None:
    """Create a database object with the right URI"""
    superset_db = get_or_create_db(database_name, uri, always_create=True)
    db.session.add(superset_db)
    db.session.commit()


def create_zip_and_import_assets():
    with ZipFile(ZIP_PATH, "w") as zip:
        for folder in ASSET_FOLDER_MAPPING.values():
            for file_name in os.listdir(f"{BASE_DIR}/{folder}"):
                zip.write(
                    f"{BASE_DIR}/{folder}/{file_name}", f"import/{folder}/{file_name}"
                )
        zip.write(f"{BASE_DIR}/metadata.yaml", "import/metadata.yaml")
        contents = get_contents_from_bundle(zip)
        command = ImportAssetsCommand(contents)
        command.run()

    os.remove(ZIP_PATH)


def update_dashboard_roles(roles):
    for dashboard_uuid, role_ids in roles.items():
        dashboard = db.session.query(Dashboard).filter_by(uuid=dashboard_uuid).one()
        dashboard.roles = role_ids
        dashboard.published = True
        db.session.commit()


if __name__ == "__main__":
    main()
