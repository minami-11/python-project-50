import json


def format(data):
    '''Make valid json string from input data'''

    result_string = json.dumps(data)
    return result_string
