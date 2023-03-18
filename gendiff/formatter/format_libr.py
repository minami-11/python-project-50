def is_dict(value) -> bool:
    """Return True if value is dictionary, else False"""
    return isinstance(value, dict)


def is_list(value) -> bool:
    """Return True if value is list, else False"""
    return isinstance(value, list)


def shift(deep, variable: int = 2):
    return ' ' * (4 * deep - variable)


def get_node_value(item: dict):
    if is_dict(item) and 'children' in item:
        return item['children']
    else:
        raise ValueError('Check item type or item keys')


def get_change_mark(value) -> str:
    '''Return modified mark if value is node'''
    if is_dict(value):
        return value['modified']
    else:
        return ''
