def is_dict(value) -> bool:
    """Return True if value is dictionary, else False"""
    return isinstance(value, dict)


def shift(deep, variable: int = 2):
    return ' ' * (4 * deep - variable)


def get_node_value(item: dict):
    if is_dict(item) and 'children' in item:
        return item['children']
    else:
        raise ValueError('Check item type or item keys')


def get_node_type(item: dict):
    if is_dict(item) and 'type' in item:
        return item['type']
    else:
        raise ValueError('Check item type or item keys')


def pass_through_converter(value):
    '''Return valid value'''
    converter = {
        'True': 'true',
        'False': 'false',
        'None': 'null'
    }
    return converter.get(str(value), value)
