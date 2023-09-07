import yaml

def get_config(file: str) -> dict:
    with open(file, 'r', encoding = "utf-8") as f:
        data = yaml.load(f, yaml.FullLoader)
    return data