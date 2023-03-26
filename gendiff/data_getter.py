from os import SEEK_SET
from gendiff.parser import parse


def get_data_from_source(origin_):
    '''Parse data from origin'''
    origin = str(origin_)
    with open(origin, 'r') as file:
        data = file.read()
        file.seek(SEEK_SET, 0)
    if origin.endswith('json'):
        return parse(data, 'json')
    elif origin.endswith('yaml') or origin.endswith('yml'):
        return parse(data, 'yaml')
    else:
        raise TypeError('Get ERROR. Check the file type.')
