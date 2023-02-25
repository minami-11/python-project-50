import json


def get_json_from_file(file_1: str, file_2: str):
    '''Return data from two json files'''
    with open(file_1, 'r') as f_1:
        with open(file_2, 'r') as f_2:
            data_1 = json.load(f_1)
            data_2 = json.load(f_2)
    return data_1, data_2


def normalize(value):
    '''Bring value to normal'''
    converter = {
        'True': 'true',
        'False': 'false',
        'None': 'null'
    }
    return converter[str(value)] if str(value) in converter else value


def match_difference(origin, sample_1, sample_2) -> list:
    final_list = []

    for key, value in sorted(origin.items()):
        if key in sample_2 and key not in sample_1:
            final_list.append(f'  + {key}: {normalize(value)}')
        elif key in sample_2 and value == sample_2.get(key):
            final_list.append(f'    {key}: {normalize(value)}')
        elif key in sample_2 and value != sample_2.get(key):
            final_list.append(f'  - {key}: {normalize(value)}')
            final_list.append(f'  + {key}: {normalize(sample_2.get(key))}')
        elif key in sample_1 and key not in sample_2:
            final_list.append(f'  - {key}: {normalize(value)}')

    return final_list


def generate_diff(file_path_1: str, file_path_2: str):
    '''Return differences between to files'''
    data1, data2 = get_json_from_file(file_path_1, file_path_2)
    list_start = ['{']
    list_end = ['}']
    new_data = new_data = dict(data2 | data1)
    result_list = list_start + match_difference(new_data,
                                                data1, data2) + list_end

    # with open('result.json', 'w') as result_file:
    #     json.dump(new_data, result_file, indent=3)

    return '\n'.join(result_list)
