def is_dict(value) -> bool:
    """Return True if value is dictionary, else False"""
    return isinstance(value, dict)


def shift(deep, variable: int = 2):
    return ' ' * (4 * deep - variable)


def get_change_mark(value) -> str:
    '''Return modified mark if value is node'''
    if is_dict(value):
        return value['modified']
    else:
        return ''


def get_finish_line(income):
    output = []
    if not isinstance(income, (dict, list)):
        return income
    if is_dict(income) and not isinstance(income['children'], (list, dict)):
        output.append(f"{shift(income['depth'])}{income['modified']}"
                      f"{income['name']}: {income['children']}")
    else:
        output.append(use_stylish_format(income))
    return '\n'.join(output)


def use_stylish_format(income_list) -> str:
    '''Format input string in stylish way'''
    if not income_list:
        return '{}'
    output = []
    output.append('{')
    for item in income_list:
        mark = get_change_mark(item)

        if all([is_dict(item), isinstance(item['children'], list),
                mark == "-+"]):
            output.append(f"{shift(item['depth'])}- {item['name']}: "
                          f"{get_finish_line(item['children'][0])}")
            output.append(f"{shift(item['depth'])}+ {item['name']}: "
                          f"{get_finish_line(item['children'][1])}")

        elif is_dict(item) and isinstance(item['children'], list):
            output.append(f"{shift(item['depth'])}{mark}{item['name']}: "
                          f"{use_stylish_format(item['children'])}")
        else:
            output.append(f"{get_finish_line(item)}")

    output.append(f"{shift(item['depth'] - 1, 0)}" + '}')
    return '\n'.join(map(lambda x: x.rstrip(), output))
