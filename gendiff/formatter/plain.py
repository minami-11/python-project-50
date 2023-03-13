from ..formatter.stylish import is_dict


def normalize(value):
    '''Bring value to the required output parameters'''

    if is_dict(value):
        return "[complex value]"
    converter = {
        'True': 'true',
        'False': 'false',
        'None': 'null'
    }
    return converter.get(str(value), f"'{value}'")


def format_in_plain(data_1, data_2, key):
    '''Output result gets plain'''
    value_1 = data_1.get(key)
    value_2 = data_2.get(key)
    if key in data_2 and key not in data_1:
        return f"was added with value: {normalize(value_2)}"
    elif key in data_2 and value_1 != value_2:
        return f"was updated. From {normalize(value_1)} to {normalize(value_2)}"
    elif key in data_1 and key not in data_2:
        return 'was removed'
    return ''


def use_plain_logic(data_1, data_2, storage_, key, walk):
    value_1 = data_1.get(key)
    value_2 = data_2.get(key)
    if all(map(is_dict, [value_1, value_2])):
        mediate_path = storage_ + '.' * (bool(storage_)) + str(key)
        return f"{walk(value_1, value_2, mediate_path)}"
    else:
        if format_in_plain(data_1, data_2, key):
            return f"Property '{storage_}{'.' * (bool(storage_))}{key}' " \
                   f"{format_in_plain(data_1, data_2, key)}"
