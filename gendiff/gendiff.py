import json
import yaml
from os import SEEK_SET

# from parser import parse_for_differences
from gendiff.parser import parse_for_differences


def get_data_from_file(file_path: str) -> dict:
    '''Return data from not empty files (with correct file type)'''
    with open(file_path, 'r') as file:
        data = file.read()
        file.seek(SEEK_SET, 0)
        if file_path.endswith('.json'):
            output_data = json.load(file) if data else {}
        elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
            output_data = yaml.safe_load(file) if data else {}
        else:
            raise TypeError('Get ERROR. Check the file type.')
        return output_data


def generate_diff(file_1: str, file_2: str, format: str = 'stylish') -> None:
    '''Compare two files and match differences between them'''

    dict_1, dict_2 = list(map(get_data_from_file, (str(file_1), str(file_2))))

    diff_string = parse_for_differences(dict_1, dict_2, format)

    with open('result.txt', 'w') as txt:
        print(diff_string, file=txt)
