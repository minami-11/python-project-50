import json
import yaml


def parse(data: str, extension: str) -> dict:
    if extension == 'json':
        output_data = json.loads(data) if data else {}
    elif extension == 'yaml':
        output_data = yaml.safe_load(data) if data else {}
    return output_data
