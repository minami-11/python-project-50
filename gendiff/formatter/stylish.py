from ..formatter.format_libr import is_dict, is_list, shift, get_change_mark
from ..formatter.format_libr import get_node_value as node_value


def make_shift_line(item: dict, mark, func=(lambda x: x)):
    if mark == '-+':
        return [f"{shift(item['depth'])}- {item['name']}: "
                f"{func(node_value(item)[0])}",
                f"{shift(item['depth'])}+ {item['name']}: "
                f"{func(node_value(item)[1])}"
                ]
    return f"{shift(item['depth'])}{mark}" \
           f"{item['name']}: {func(node_value(item))}"


def normalize(income):
    output = []
    if not isinstance(income, (dict, list)):
        return income
    if is_dict(income) and not isinstance(node_value(income), (list, dict)):
        output.append(make_shift_line(income, get_change_mark(income)))
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

        if all([is_dict(item), is_list(node_value(item)), mark == "-+"]):
            output.extend(make_shift_line(item, mark, normalize))
        elif is_dict(item) and is_list(node_value(item)):
            output.append(make_shift_line(item, mark, use_stylish_format))
        else:
            output.append(f"{normalize(item)}")

    output.append(f"{shift(item['depth'] - 1, 0)}" + '}')
    return '\n'.join(map(lambda x: x.rstrip(), output))
