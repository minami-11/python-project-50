from ..formatter.format import is_dict
from ..formatter.format import get_node_value
from ..formatter.format import get_node_type
from ..formatter.format import pass_through_converter as convert


def to_string(value):
    '''Bring value to the required output parameters'''
    if isinstance(value, (list, dict)):
        return "[complex value]"
    valid_v = convert(value)
    excludes = ('false', 'true', 'null')
    return f"'{valid_v}'" if all([valid_v not in excludes,
                                  isinstance(valid_v, str)]) else valid_v


def get_valid_conclusion(item) -> str:
    '''Return valid output conclusion'''
    node_value = get_node_value(item)
    node_type = get_node_type(item)

    match node_type:
        case 'added': return f"was added with value: " \
                             f"{to_string(node_value)}"
        case 'removed': return 'was removed'
        case 'changed':
            value_1 = to_string(node_value[0])
            value_2 = to_string(node_value[1])
            return f"was updated. From {value_1} to {value_2}"


def format(input_diff: dict) -> str:
    '''Format income raw data in plain way'''

    def walk(diff, path):
        output = []
        for key, value in diff.items():
            node_value = get_node_value(value)
            node_type = get_node_type(value)
            point = '.' * (bool(path))
            root_path = path + point + key

            if is_dict(node_value) and node_type != 'same':
                output.append(f"Property '{root_path}' "
                              f"{get_valid_conclusion(value)}")
            elif is_dict(node_value):
                output.append(f"{walk(node_value, root_path)}")
            else:
                if get_valid_conclusion(value):
                    output.append(f"Property '{root_path}' "
                                  f"{get_valid_conclusion(value)}")

        return '\n'.join(filter(None, output))
    return walk(input_diff, '')
