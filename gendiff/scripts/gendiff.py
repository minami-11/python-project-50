#!/usr/bin/python3

import argparse
from gendiff.gendiff import generate_diff

parser = argparse.ArgumentParser(description="Compares two configuration\
                                              files and shows a difference.")
parser.add_argument('first_file', type=str)
parser.add_argument('second_file', type=str)
parser.add_argument('-f', '--format', help="set format of output")

args = parser.parse_args()


def main():
    generate_diff(args.first_file, args.second_file)
    with open('result.txt', 'r') as file:
        result = file.read()
    print(result)


if __name__ == '__main__':
    main()
