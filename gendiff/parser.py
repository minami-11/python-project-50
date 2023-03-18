
def is_dict(value) -> bool:
    '''Return True if value is dictionary, else False'''
    return isinstance(value, dict)


def unpack_nested_dict(sample: dict, level) -> list:
    '''Converts nested dictionary to flat list'''
    flat_list = []
    for key, value in sample.items():
        sub_tree = {
            'name': key,
            'depth': level + 1,
            'modified': '  '
        }
        flat_list.append(sub_tree)
        if is_dict(value):
            sub_tree['children'] = unpack_nested_dict(value, level + 1)
        else:
            sub_tree['children'] = value

    return flat_list


def make_valid_data(value, deep):
    if is_dict(value):
        return unpack_nested_dict(value, deep)
    converter = {
        'True': 'true',
        'False': 'false',
        'None': 'null'
    }
    return converter.get(str(value), value)


def add_modified_marks(data_1, data_2, key, deep):
    '''Add modified marks for each data change'''
    valid_value1 = make_valid_data(data_1.get(key), deep)
    valid_value2 = make_valid_data(data_2.get(key), deep)

    sub_tree2 = {
        'name': key,
        'depth': deep
    }
    if key in data_2 and key not in data_1:
        sub_tree2['modified'] = '+ '
        sub_tree2['children'] = valid_value2
    elif key in data_2 and data_1.get(key) == data_2.get(key):
        sub_tree2['modified'] = '  '
        sub_tree2['children'] = valid_value2
    elif key in data_2 and data_1.get(key) != data_2.get(key):
        sub_tree2['modified'] = '-+'
        sub_tree2['children'] = []
        sub_tree2['children'].append(valid_value1)
        sub_tree2['children'].append(valid_value2)
    else:
        sub_tree2['modified'] = '- '
        sub_tree2['children'] = valid_value1
    return sub_tree2


def parse_for_differences(data1: dict, data2: dict) -> list:
    '''Find is there differences between two dicts and return result as list'''

    def walk(data_1, data_2, deep):
        deep += 1
        tree_list = []
        keys_set = sorted(set(data_1) | set(data_2))

        for key in keys_set:
            value_1 = data_1.get(key)
            value_2 = data_2.get(key)

            if all(map(is_dict, [value_1, value_2])):
                sub_tree = {
                    'name': key,
                    'depth': deep,
                    'modified': '  ',
                    'children': walk(value_1, value_2, deep)
                }
                tree_list.append(sub_tree)
            else:
                tree_list.append(add_modified_marks(data_1, data_2, key, deep))

        return tree_list
    return walk(data1, data2, 0)
