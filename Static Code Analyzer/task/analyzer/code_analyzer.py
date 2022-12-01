import argparse
from checker import Checker


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", default='.')
    args = parser.parse_args()
    path = args.path
    my_checker = Checker(path)
    if my_checker.select_dir_or_file() == 'file':
        my_checker.check_file()
    elif my_checker.select_dir_or_file() == 'dir':
        my_checker.check_dir()
    my_checker.print_errors()
