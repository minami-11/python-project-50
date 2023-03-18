from ..formatter.stylish import is_dict


def make_valid(value):
    '''Bring value to the required output parameters'''
    if isinstance(value, (list, dict)):
        return "[complex value]"
    excludes = ('false', 'true', 'null')
    return f"'{value}'" if value not in excludes else value


def get_plain_result(item: dict) -> str:
    '''Output result gets plain'''

    match item['modified']:
        case '+ ': return f"was added with value: " \
                          f"{make_valid(item['children'])}"
        case '- ': return 'was removed'
        case _:
            value_1 = make_valid(item['children'][0])
            value_2 = make_valid(item['children'][1])
            return f"was updated. From {value_1} to {value_2}"


def use_plain_format(input_list: list) -> str:
    '''Format input string in plain way'''
    if not input_list:
        return '{}'

    def walk(input_list, path):
        output = []

        for item in input_list:
            point = '.' * (bool(path))

            if is_dict(item) and not item['modified'].strip():
                path_ = path + point + item['name']
                output.append(f"{walk(item['children'], path_)}")
            else:
                if is_dict(item):
                    output.append(f"Property '{(path + point + item['name'])}' "
                                  f"{get_plain_result(item)}")

        return '\n'.join(filter(None, output))
    return walk(input_list, '')
