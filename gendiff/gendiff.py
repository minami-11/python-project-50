from gendiff.formatter import stylish, plain, get_json, is_dict
from gendiff.data_getter import get_data_from_source as get_data


def process_nested_dict(sample):
    '''Process single nested dict with adding change mark'''
    sub_tree = {}
    for key, value in sample.items():
        sub_tree[key] = {'type': 'same'}
        if is_dict(value):
            sub_tree[key]['children'] = process_nested_dict(value)
        else:
            sub_tree[key]['children'] = value

    return sub_tree


def add_modified_marks(data_1, data_2, key):
    '''Add modified marks for each value change'''
    value_1 = data_1.get(key)
    valid_value1 = process_nested_dict(value_1) if is_dict(value_1) else value_1
    value_2 = data_2.get(key)
    valid_value2 = process_nested_dict(value_2) if is_dict(value_2) else value_2
    sub_tree = {}

    if key in data_2 and key not in data_1:
        sub_tree['type'] = 'added'
        sub_tree['children'] = valid_value2
    elif key in data_2 and data_1.get(key) == data_2.get(key):
        sub_tree['type'] = 'same'
        sub_tree['children'] = valid_value2
    elif key in data_2 and data_1.get(key) != data_2.get(key):
        sub_tree['type'] = 'changed'
        sub_tree['children'] = []
        sub_tree['children'].append(valid_value1)
        sub_tree['children'].append(valid_value2)
    else:
        sub_tree['type'] = 'removed'
        sub_tree['children'] = valid_value1
    return sub_tree


def make_raw_variance(data_1: dict, data_2: dict):
    '''Find is there differences between two dicts and return result as list'''
    tree_dict = {}
    keys_set = sorted(set(data_1) | set(data_2))

    for key in keys_set:
        value_1 = data_1.get(key)
        value_2 = data_2.get(key)
        if all(map(is_dict, [value_1, value_2])):
            tree_dict[key] = {
                'type': 'same',
                'children': make_raw_variance(value_1, value_2)
            }
        else:
            tree_dict[key] = add_modified_marks(data_1, data_2, key)

    return tree_dict


def generate_diff(source_1: str, source_2: str, format: str = 'stylish') -> str:
    '''Compare two files and match differences between them'''
    parsed_data_1 = get_data(source_1)
    parsed_data_2 = get_data(source_2)
    raw_variance_data = make_raw_variance(parsed_data_1, parsed_data_2)

    match format:
        case 'stylish': formatted_string = stylish(raw_variance_data)
        case 'plain': formatted_string = plain(raw_variance_data)
        case 'json': formatted_string = get_json(raw_variance_data)
        case _:
            raise ValueError('Unknown format type, please check the format')

    return formatted_string
