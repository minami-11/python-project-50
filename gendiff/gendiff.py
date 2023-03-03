import json
import yaml
from os import SEEK_SET


def extract_json_yaml(file_path: str):
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


def get_data_from_file(file_1: str, file_2: str):
    '''Return data from two json files if files are not empty'''
    data_1 = extract_json_yaml(str(file_1))
    data_2 = extract_json_yaml(str(file_2))
    return data_1, data_2


def normalize(value):
    '''Bring value to the required parameters'''
    converter = {
        'True': 'true',
        'False': 'false',
        'None': 'null'
    }
    return converter.get(str(value), value)


def match_difference(merged, sample_1, sample_2) -> list:
    output = []

    for key, value in sorted(merged.items()):
        item_pair = f'{key}: {normalize(value)}'
        if key in sample_2 and key not in sample_1:
            output.append('  + ' + item_pair)
        elif key in sample_2 and value == sample_2.get(key):
            output.append('    ' + item_pair)
        elif key in sample_2 and value != sample_2.get(key):
            output.append('  - ' + item_pair)
            output.append(f'  + {key}: {normalize(sample_2.get(key))}')
        else:
            output.append('  - ' + item_pair)

    return output


def generate_diff(file_path_1: str, file_path_2: str) -> None:
    '''Return differences between to files'''

    data1, data2 = get_data_from_file(file_path_1, file_path_2)
    string_start = '{'
    string_end = '}'
    merged_data = dict(data2 | data1)
    diff_string = '\n'.join(match_difference(merged_data, data1, data2))

    with open('result.txt', 'w') as txt:
        if diff_string:
            print(string_start, diff_string, string_end, file=txt, sep='\n')
        else:
            print(string_start.strip() + diff_string + string_end.strip(),
                  file=txt)
