from gendiff.formatter import get_shift, use_stylish, use_plain


def choose_formatter_logic(format: str = 'stylish'):
    format_catalog = {
        'plain' == format: use_plain,
        'stylish' == format: use_stylish
    }
    return format_catalog[True]


def parse_for_differences(data1: dict, data2: dict, format: str = 'stylish'):
    '''Find is there differences between 2 dicts and return string result'''
    match format:
        case 'plain': storage = ''
        case _: storage = 0

    def walk(data_1, data_2, storage_):

        output = []
        if format == 'stylish':
            storage_ += 1
            output.append('{')
        keys_set = sorted(set(data_1) | set(data_2))
        # if not keys_set:
        #     return '{}'
        for key in keys_set:
            result_string = choose_formatter_logic(format)(data_1,
                                                           data_2, storage_,
                                                           key, walk)
            output.append(result_string)
        if format == 'stylish':
            output.append(get_shift(storage_ - 1, 0) + '}')

        return '\n'.join(filter(None, output)) if keys_set else '{}'
    return walk(data1, data2, storage)
