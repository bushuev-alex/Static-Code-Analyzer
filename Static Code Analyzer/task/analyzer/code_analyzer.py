import argparse
from checker import Checker


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", default='.')
    args = parser.parse_args()
    my_checker = Checker(args.path)
    if my_checker.check_if_dir():
        my_checker.check_dir()
    else:
        my_checker.check_file()
    my_checker.print_errors()
