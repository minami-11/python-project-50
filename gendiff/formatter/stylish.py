def is_dict(value) -> bool:
    """Return True if value is dictionary, else False"""
    return isinstance(value, dict)


def get_shift(deep, variable=2):
    return ' ' * (4 * deep - variable)


def normalize(value, deep: (int | float) = None, format: str = 'stylish'):
    '''Bring value to the required output parameters'''

    if is_dict(value):
        open_char = '{'
        close_char = get_shift(deep, 0) + '}'
        return '\n'.join([open_char] + unpack_dict(value, deep) + [close_char])
    converter = {
        'True': 'true',
        'False': 'false',
        'None': 'null'
    }
    return converter.get(str(value), value)


def unpack_dict(sample: dict, level: (int | float)) -> list:
    '''Converts nested dictionary to flat list'''
    output = []
    shift = get_shift(level + 1, 0)
    for key, value in sample.items():
        if is_dict(value):
            output += [shift + f'{key}: ' + '{']
            output += unpack_dict(value, level + 1)
            output.append(shift + '}')
        else:
            output.append(shift + f'{key}: {value}')
    return output


def format_in_stylish(data_1, data_2, key, deep) -> str:
    '''Mark differences and add stylish shift to output string'''
    value_1 = f'{key}: {normalize(data_1.get(key), deep)}'.strip()
    value_2 = f'{key}: {normalize(data_2.get(key), deep)}'.strip()
    shift = get_shift(deep)
    if key in data_2 and key not in data_1:
        return shift + '+ ' + value_2
    elif key in data_2 and data_1.get(key) == data_2.get(key):
        return shift + '  ' + value_2
    elif key in data_2 and data_1.get(key) != data_2.get(key):
        return '\n'. join((shift + '- ' + value_1,
                          shift + '+ ' + value_2))
    else:
        return shift + '- ' + value_1


def use_stylish_logic(data_1, data_2, deep, key, walk):
    value_1 = data_1.get(key)
    value_2 = data_2.get(key)
    if all(map(is_dict, [value_1, value_2])):
        return f'{get_shift(deep)}  {key}: ' + walk(value_1,
                                                    value_2, deep)
    else:
        return format_in_stylish(data_1, data_2, key, deep)
