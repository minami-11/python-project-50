import json
import yaml
from os import SEEK_SET


def is_dict(value) -> bool:
    """Return True if value is dictionary, else False"""
    return isinstance(value, dict)


def unpack_dict(sample: dict, level: (int | float)) -> list:
    '''Converts nested dictionary to flat list'''
    output = []
    shift = ' ' * 4 * (level + 1)
    for key, value in sample.items():
        if is_dict(value):
            output += [shift + f'{key}: ' + '{']
            output += unpack_dict(value, level + 1)
            output.append(shift + '}')
        else:
            output.append(shift + f'{key}: {value}')
    return output


def normalize(value, deep: (int | float)):
    '''Bring value to the required output parameters'''
    if is_dict(value):
        open_char = '{'
        close_char = '}'
        return '\n'.join([open_char] + unpack_dict(value, deep) +
                         [' ' * 4 * deep + close_char])
    converter = {
        'True': 'true',
        'False': 'false',
        'None': 'null'
    }
    return converter.get(str(value), value)


def stylish(data_1, data_2, key, deep) -> str:
    '''Mark differences and add stylish shift to output string'''
    value_1 = f'{key}: {normalize(data_1.get(key), deep)}'.strip()
    value_2 = f'{key}: {normalize(data_2.get(key), deep)}'.strip()
    shift = ' ' * (4 * deep - 2)
    if key in data_2 and key not in data_1:
        return shift + '+ ' + value_2
    elif key in data_2 and data_1.get(key) == data_2.get(key):
        return shift + '  ' + value_2
    elif key in data_2 and data_1.get(key) != data_2.get(key):
        return '\n'. join((shift + '- ' + value_1,
                          shift + '+ ' + value_2))
    else:
        return shift + '- ' + value_1


def get_differences(data_1: dict, data_2: dict) -> str:
    '''Find is there differences between two dicts and return string result'''

    def walk(data_1, data_2, depth):
        depth += 1
        outturn = []
        outturn.append('{')
        shift = ' ' * (4 * depth - 2)
        keys_set = sorted(set(data_1) | set(data_2))
        if not keys_set:
            return '{}'
        for key in keys_set:
            value_1 = data_1.get(key)
            value_2 = data_2.get(key)
            if all(map(is_dict, [value_1, value_2])):
                outturn.append(f'{shift}  {key}: ' + walk(value_1,
                                                          value_2, depth))
            else:
                outturn.append(stylish(data_1, data_2, key, depth))
        outturn.append(' ' * (4 * (depth - 1)) + '}')
        return '\n'.join(outturn)

    return walk(data_1, data_2, 0)


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


def generate_diff(file_1: str, file_2: str) -> None:
    '''Compare two files and match differences between them'''

    dict_1, dict_2 = list(map(get_data_from_file, (str(file_1), str(file_2))))

    diff_string = get_differences(dict_1, dict_2)

    with open('result.txt', 'w') as txt:
        print(diff_string, file=txt)
