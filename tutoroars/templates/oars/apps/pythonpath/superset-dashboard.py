#!/usr/bin/env python
"""
Uses Superset's REST API to create the OARS datastores, charts, and dashboard.
"""
import os
import zipfile
import tempfile
import datetime
from supersetapiclient.client import SupersetClient


SUPERSET_URL_SCHEME = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}"
SUPERSET_HOST_URL = f"{SUPERSET_URL_SCHEME}://superset:{{ SUPERSET_PORT }}"
SUPERSET_ADMIN_USERNAME = "{{ SUPERSET_ADMIN_USERNAME }}"
SUPERSET_ADMIN_PASSWORD = "{{ SUPERSET_ADMIN_PASSWORD }}"
SUPERSET_DATA_ASSETS_DIR = "/app/oars/data/assets/"
SUPERSET_DB_PASSWORDS = {
    # Database names neet to match file names under SUPERSET_DATA_ASSETS_DIR/databases/
    "OpenedX_MySQL": "{{ OPENEDX_MYSQL_PASSWORD }}",
    "OpenedX_Clickhouse": "{{ OARS_CLICKHOUSE_REPORT_PASSWORD }}",
}
OPENEDX_DASHBOARD_SLUG = "{{ SUPERSET_XAPI_DASHBOARD_SLUG }}"

def update_assets():
    # Need to override this setting to allow OAuth over http
    if SUPERSET_URL_SCHEME == 'http':
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        verify=False
    else:
        verify=True

    superset = SupersetClient(
        host=SUPERSET_HOST_URL,
        username=SUPERSET_ADMIN_USERNAME,
        password=SUPERSET_ADMIN_PASSWORD,
        verify=verify,
    )

    # Import the assets as zip files.
    # We do this for each individual asset type so we can overwrite them. We could just zip up the whole asset dir and
    # import it using the Dashboards import, but this only overwrites the Dashboard, nothing else.
    superset_assets = {
        'databases': 'Database',
        'datasets': 'SqlaTable',
        'charts': 'Slice',
        'dashboards': 'Dashboard',
    }
    for asset_type, metadata_type in superset_assets.items():
        zip_file = superset_asset_zip(
            SUPERSET_DATA_ASSETS_DIR,
            asset_type=asset_type,
            metadata_type=metadata_type,
        )
        getattr(superset, asset_type).import_file(
            zip_file.name,
            overwrite=True,
            passwords=SUPERSET_DB_PASSWORDS,
        )
        # Remove the temporary zipfile
        os.unlink(zip_file.name)

    # Mark the imported dashboard as Published
    dashboard = superset.dashboards.find(slug=OPENEDX_DASHBOARD_SLUG)[0]
    dashboard.published = True
    # TODO: Enable feature flag DASHBOARD_RBAC, and set dashboard.roles = ["Open edX"]
    # Consider finishing https://github.com/opus-42/superset-api-client/pull/31
    dashboard.save()


def superset_asset_zip(zip_dir, asset_type, metadata_type, metadata_version='1.0.0'):
    """
    Zips up the contents of the given dir to a temporary file,
    adding in the expected metadata.yaml file for the given asset type.

    Returns the temporary file pointer to the zip file.
    """
    fp = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
    asset_dir = os.path.abspath(zip_dir)
    archive_base_dir = asset_type
    timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    with zipfile.ZipFile(fp, "w") as ziph:  # ziph is zipfile handle
        # Write a metadata.yaml file to the root dir
        ziph.writestr(os.path.join(archive_base_dir, 'metadata.yaml'),
            f"version: {metadata_version}\n"
            f"type: {metadata_type}\n"
            f"timestamp: '{timestamp}'\n"
        )

        for root, dirs, files in os.walk(asset_dir):
            if root == asset_dir:
                archive_dir = archive_base_dir
            else:
                archive_dir = os.path.join(archive_base_dir, os.path.relpath(root, asset_dir))
                # Add this subdir to the zip file
                ziph.write(root, arcname=archive_dir)

            # Add all the files in root to the zip file
            for file in files:
                ziph.write(
                    os.path.join(root, file),
                    arcname=os.path.join(archive_dir, file),
                )
    fp.close()
    return fp


if __name__ == "__main__":
    update_assets()
