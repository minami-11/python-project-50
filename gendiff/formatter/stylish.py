from ..formatter.format import is_dict, shift
from ..formatter.format import get_node_value
from ..formatter.format import get_node_type
from ..formatter.format import pass_through_converter as convert


def get_type_mark(income: dict):
    '''Convert raw modified type to char mark'''
    type_converter = {
        'same': '  ',
        'added': '+ ',
        'removed': '- '
    }
    node_type = get_node_type(income)
    return type_converter.get(node_type)


def make_valid(value):
    '''Make valid value from income data'''
    valid_value = convert(value)
    return valid_value


def format(input_diff: dict) -> str:
    '''Format income raw data in stylish way'''

    def walk(diff, deep):
        deep += 1
        output = ['{']

        if not is_dict(diff):
            return make_valid(diff)
        for key, value in diff.items():
            mark = get_type_mark(value)
            marked_name = f"{shift(deep)}{mark}{key}"
            node_value = get_node_value(value)
            node_type = get_node_type(value)

            if is_dict(node_value) and node_type != 'changed':
                output.append(f"{marked_name}: {walk(node_value, deep)}")
            elif node_type == 'changed':
                output.append(f"{shift(deep)}- {key}: "
                              f"{walk(node_value[0], deep)}")
                output.append(f"{shift(deep)}+ {key}: "
                              f"{walk(node_value[1], deep)}")
            else:
                output.append(f"{marked_name}: {make_valid(node_value)}")

        output.append(f"{shift(deep - 1, 0)}" + '}')
        new_line = '\n' * bool(diff)
        return new_line.join(output)
    return walk(input_diff, 0)
