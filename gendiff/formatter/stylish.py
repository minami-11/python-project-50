from ..formatter.format_libr import is_dict, shift
from ..formatter.format_libr import get_node_value
from ..formatter.format_libr import get_node_type
from ..formatter.format_libr import pass_through_converter as convert


def get_type_mark(income: dict):
    '''Convert raw modified type to char mark'''
    type_converter = {
        'same': '  ',
        'added': '+ ',
        'removed': '- '
    }
    node_type = get_node_type(income)
    return type_converter.get(node_type)


def make_valid(value, deep):
    '''Make valid value from income data'''
    if is_dict(value):
        return use_stylish_format(value, deep)
    valid_value = convert(value)
    return valid_value


def use_stylish_format(income: dict, deep: int = 0) -> str:
    '''Format income raw data in stylish way'''
    if not income:
        return ''
    deep += 1
    output = ['{']

    for key, value in income.items():
        mark = get_type_mark(value)
        marked_name = f"{shift(deep)}{mark}{key}"
        node_value = get_node_value(value)
        node_type = get_node_type(value)

        if is_dict(node_value) and node_type != 'changed':
            output.append(f"{marked_name}: "
                          f"{use_stylish_format(node_value, deep)}")
        elif node_type == 'changed':
            output.append(f"{shift(deep)}- {key}: "
                          f"{make_valid(node_value[0], deep)}")
            output.append(f"{shift(deep)}+ {key}: "
                          f"{make_valid(node_value[1], deep)}")
        else:
            output.append(f"{marked_name}: {make_valid(node_value, deep)}")

    output.append(f"{shift(deep - 1, 0)}" + '}')
    return '\n'.join(output)
