#!/usr/bin/python3

import argparse
from gendiff import generate_diff


parser = argparse.ArgumentParser(description="Compares two configuration\
                                              files and shows a difference.")
parser.add_argument('first_file', type=str)
parser.add_argument('second_file', type=str)
parser.add_argument('-f', '--format', type=str,
                    help="output format (default: 'stylish')",
                    default="stylish")

args = parser.parse_args()


def main():
    generate_diff(args.first_file, args.second_file, args.format)


if __name__ == '__main__':
    main()
