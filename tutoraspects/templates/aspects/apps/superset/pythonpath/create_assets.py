"""Import a list of assets from a yaml file and create them in the superset assets folder."""
import os
import uuid
from zipfile import ZipFile

import yaml
from superset.app import create_app

app = create_app()
app.app_context().push()

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

FILE_NAME_ATTRIBUTE = "_file_name"

translations = yaml.load(
    open("/app/pythonpath/locale.yaml", "r"), Loader=yaml.FullLoader
)


def main():
    create_assets()


def create_assets():
    """Create assets from a yaml file."""
    roles = {}
    with open("/app/pythonpath/assets.yaml", "r") as file:
        extra_assets = yaml.safe_load(file)

        if not extra_assets:
            print("No extra assets to create")
            return

        # For each asset, create a file in the right folder
        for asset in extra_assets:
            if FILE_NAME_ATTRIBUTE not in asset:
                print(f"Asset {asset} has no _file_name")
                continue
            file_name = asset.pop(FILE_NAME_ATTRIBUTE)

            # Find the right folder to create the asset in
            for asset_name, folder in ASSET_FOLDER_MAPPING.items():
                if asset_name in asset:
                    if folder == "databases":
                        # This will fix the URI connection string by setting the right password.
                        create_superset_db(
                            asset["database_name"], asset["sqlalchemy_uri"]
                        )
                    elif folder == "dashboards":
                        dashboard_roles = asset.pop("_roles", None)
                        if dashboard_roles:
                            roles[asset["uuid"]] = [
                                security_manager.find_role(role)
                                for role in dashboard_roles
                            ]

                    write_asset_to_file(asset, folder, file_name, roles)
                    break

    # Create the zip file and import the assets
    zip_path = "/app/assets/assets.zip"
    with ZipFile(zip_path, "w") as zip:
        for folder in ASSET_FOLDER_MAPPING.values():
            for file_name in os.listdir(f"{BASE_DIR}/{folder}"):
                zip.write(
                    f"{BASE_DIR}/{folder}/{file_name}", f"import/{folder}/{file_name}"
                )
        zip.write(f"{BASE_DIR}/metadata.yaml", "import/metadata.yaml")

        contents = get_contents_from_bundle(zip)
        command = ImportAssetsCommand(
            contents,
        )

        command.run()

    os.remove(zip_path)
    
    # Create the roles
    for dashboard_uuid, role_ids in roles.items():
        dashboard = db.session.query(Dashboard).filter_by(uuid=dashboard_uuid).one()
        dashboard.roles = role_ids
        dashboard.published = True
        db.session.commit()


def get_uuid5(base_uuid, name):
    """Generate an idempotent uuid."""
    base_uuid = uuid.UUID(base_uuid)
    base_namespace = uuid.uuid5(base_uuid, "superset")
    return uuid.uuid5(base_namespace, name)


def write_asset_to_file(asset, folder, file_name, roles):
    """Write an asset to a file."""
    path = f"{BASE_DIR}/{folder}/{file_name}.yaml"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file = open(path, "w")
    with open(path, "w") as file:
        yaml.dump(asset, file)

    asset_translation = translations.get(asset.get("uuid"))
    
    if not asset_translation:
        return

    for language, title in asset_translation.items():
        copy = asset.copy()
        copy["uuid"] = str(get_uuid5(copy["uuid"], language))

        print(f"\n\nCreating translation for {asset.get('uuid')}, {copy.get('uuid')} in {language}: {title}\n\n")

        if folder == "dashboards":
            copy["dashboard_title"] = title
            copy["slug"] = f"{copy['slug']}-{language}"
            dashboard_roles = copy.pop("_roles", None)
            if dashboard_roles:
                dashboard_roles.append(f"{{SUPERSET_ROLES_MAPPING.instructor}} - {language}")
                roles[copy["uuid"]] = [
                    security_manager.find_role(role) for role in dashboard_roles
                ]
        elif folder == "charts":
            copy["slice_name"] = title
        elif folder == "datasets":
            copy["table_name"] = title
        elif folder == "databases":
            copy["database_name"] = title

        path = f"{BASE_DIR}/{folder}/{file_name}-{language}.yaml"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file = open(path, "w")

        with open(path, "w") as file:
            yaml.dump(copy, file)


def create_superset_db(database_name, uri) -> None:
    """Create a database object with the right URI"""
    superset_db = get_or_create_db(database_name, uri, always_create=True)
    db.session.add(superset_db)
    db.session.commit()


if __name__ == "__main__":
    main()
