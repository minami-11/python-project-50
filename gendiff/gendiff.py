import json
from os import SEEK_SET


def get_json_from_file(file_1: str, file_2: str):
    '''Return data from two json files if files are not empty'''
    with open(file_1, 'r') as f1:
        with open(file_2, 'r') as f2:
            data = f1.read()
            f1.seek(SEEK_SET, 0)
            data_1 = json.load(f1) if data else {}
            data = f2.read()
            f2.seek(SEEK_SET, 0)
            data_2 = json.load(f2) if data else {}
    return data_1, data_2


def normalize(value):
    '''Bring value to the required parameters'''
    converter = {
        'True': 'true',
        'False': 'false',
        'None': 'null'
    }
    return converter[str(value)] if str(value) in converter else value


def match_difference(merged, sample_1, sample_2) -> list:
    output = []

    for key, value in sorted(merged.items()):
        if key in sample_2 and key not in sample_1:
            output.append(f'  + {key}: {normalize(value)}')
        elif key in sample_2 and value == sample_2.get(key):
            output.append(f'    {key}: {normalize(value)}')
        elif key in sample_2 and value != sample_2.get(key):
            output.append(f'  - {key}: {normalize(value)}')
            output.append(f'  + {key}: {normalize(sample_2.get(key))}')
        elif key in sample_1 and key not in sample_2:
            output.append(f'  - {key}: {normalize(value)}')

    return output


def generate_diff(file_path_1: str, file_path_2: str) -> None:
    '''Return differences between to files'''

    data1, data2 = get_json_from_file(file_path_1, file_path_2)
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
