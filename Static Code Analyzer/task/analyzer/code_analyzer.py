import argparse
from checker import Checker


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", default='.')
    args = parser.parse_args()
    path = args.path
    my_checker = Checker(path)
    my_checker.check_dir_or_file()
    my_checker.print_errors()
