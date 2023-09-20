from .encryp import Hasher, from_pkl, to_pkl
import yaml


def read_yaml(file_name: str, encoding = "utf-8") -> dict:
    with open(file_name, "r", encoding = encoding) as f:
        data = yaml.load(f, Loader = yaml.FullLoader)
    return data

def write_yaml(file_name: str, obj: object, encoding = "utf-8") -> None:
    with open(file_name, "w", encoding = encoding) as f:
        yaml.dump(obj, f, indent = 4)