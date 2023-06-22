"""Import a list of assets from a yaml file and create them in the superset assets folder."""
import os

import yaml
from superset.app import create_app
from superset.extensions import db
from superset.utils.database import get_or_create_db

app = create_app()
app.app_context().push()
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
            print(f"Creating asset {file_name}")

            # Find the right folder to create the asset in
            for asset_name, folder in ASSET_FOLDER_MAPPING.items():
                if asset_name in asset:
                    create_asset(folder, file_name, asset)
                    break


def create_asset(folder, file_name, asset_definition):
    """Create an asset in the superset assets folder."""
    path = f"{BASE_DIR}/{folder}/{file_name}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file = open(path, "w")
    yaml.dump(asset_definition, file)
    file.close()
    print(f"Successfully created file {file_name}")

    if folder == "databases":
        # This will fix the URI connection string by setting the right password.
        create_superset_db(
            asset_definition["database_name"], asset_definition["sqlalchemy_uri"]
        )


def create_superset_db(database_name, uri) -> None:
    """Create a database object with the right URI"""
    superset_db = get_or_create_db(database_name, uri, always_create=True)
    db.session.add(superset_db)
    db.session.commit()


if __name__ == "__main__":
    main()
