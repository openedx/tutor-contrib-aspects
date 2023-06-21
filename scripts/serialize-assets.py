from zipfile import ZipFile
import sys
import yaml
import os


def serialize_assets(path):
    """Given a .zip file of assets, create a yaml file with the assets."""
    dump = []
    with ZipFile(path) as zip_file:
        for asset_path in zip_file.namelist():
            with zip_file.open(asset_path) as asset_file:
                x = yaml.safe_load(asset_file)
                x["file_name"] = os.path.basename(asset_path)
                dump.append(x)
    
    with open("assets.yaml", "w") as f:
        yaml.dump(dump, f)

    

if __name__ == "__main__":
    serialize_assets(path=sys.argv[1])
