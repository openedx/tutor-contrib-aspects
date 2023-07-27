"""Import a list of assets from a yaml file and create them in the superset assets folder."""
import os
from zipfile import ZipFile

import yaml
from superset.app import create_app

app = create_app()
app.app_context().push()

from superset.commands.importers.v1.assets import ImportAssetsCommand
from superset.commands.importers.v1.utils import get_contents_from_bundle
from superset.extensions import db
from superset.models.dashboard import Dashboard
from superset.utils.database import get_or_create_db

from superset import security_manager

BASE_DIR = "/app/assets/superset"

ASSET_FOLDER_MAPPING = {
    "dashboard_title": "dashboards",
    "slice_name": "charts",
    "database_name": "databases",
    "table_name": "datasets",
}

FILE_NAME_ATTRIBUTE = "_file_name"


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
                            roles[asset["uuid"]] = [security_manager.find_role(role) for role in dashboard_roles]

                    path = f"{BASE_DIR}/{folder}/{file_name}"
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    file = open(path, "w")
                    yaml.dump(asset, file)
                    file.close()
                    break

    # Create the zip file and import the assets
    zip_path = "/app/assets/assets.zip"
    with ZipFile(zip_path, "w") as zip:
        for folder in ASSET_FOLDER_MAPPING.values():
            for file_name in os.listdir(f"{BASE_DIR}/{folder}"):
                zip.write(f"{BASE_DIR}/{folder}/{file_name}", f"import/{folder}/{file_name}")
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


def create_superset_db(database_name, uri) -> None:
    """Create a database object with the right URI"""
    superset_db = get_or_create_db(database_name, uri, always_create=True)
    db.session.add(superset_db)
    db.session.commit()


if __name__ == "__main__":
    main()
