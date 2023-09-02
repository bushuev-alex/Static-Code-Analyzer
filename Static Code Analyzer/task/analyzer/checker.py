import re
import os
import ast
from check_methods import LineByLineChecker, ASTChecker


class Checker(LineByLineChecker, ASTChecker):

    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path

    def reset_blank_line_count(self, line: str) -> None:
        if line.strip() != '':
            self.blank_line_count = 0

    def check_line_by_line(self, line_no: int, line: str, path: str) -> None:
        self.reset_blank_line_count(line)
        self.error_s001(line_no, line, path)  # Too long
        self.error_s002(line_no, line, path)  # Indentation is not a multiple of four
        self.error_s003(line_no, line, path)  # Unnecessary semicolon after a statement
        self.error_s004(line_no, line, path)  # Less than two spaces before inline comments
        self.error_s005(line_no, line, path)  # TO_DO found (in comments only and case-insensitive)
        self.error_s006(line_no, line, path)  # More than two blank lines preceding a code line
        self.error_s007(line_no, line, path)  # Too many spaces after construction_name (def or class)
        self.error_s008(line_no, line, path)  # Class name {} should be written in CamelCase
        self.error_s009(line_no, line, path)  # Function name {} should be written in snake_case

    def check_ast_nodes(self, file, path: str) -> None:
        text = file.read()
        tree = ast.parse(text)
        nodes = ast.walk(tree)
        for node in nodes:
            if isinstance(node, ast.FunctionDef):
                for obj in node.args.args:  # Argument name {} should be written in snake_case
                    self.check_node_in_snake_case(obj, path)
                for obj in node.body:  # Variable {} should be written in snake_case
                    self.check_variable_in_snake_case(obj, path)
                for default in node.args.defaults:  # The default argument value is mutable
                    self.check_default_argument_mutable(default, path)

    def check_file(self, path_to_file=None) -> None:
        if not path_to_file:
            path_to_file = self.path
        if re.match('.*\\.py$', path_to_file):
            # Line-by-line checkers
            with open(path_to_file, 'r', encoding="UTF-8") as file:
                for n_line, line in enumerate(file, start=1):
                    self.check_line_by_line(n_line, line, path_to_file)
            # AST node checkers
            with open(path_to_file, 'r', encoding="UTF-8") as file:
                self.check_ast_nodes(file, path_to_file)

    def check_dir(self) -> None:
        file_list = os.listdir(self.path)
        file_list.sort()
        for file in file_list:
            path_to_file = self.path + f'{os.sep}' + file
            self.check_file(path_to_file)

    def check_if_dir(self) -> bool:
        if os.path.isdir(self.path):
            return True
        return False

    def print_errors(self) -> None:
        self.errors.sort(key=lambda element: (element[2], element[0], element[1]))
        for error in self.errors:
            print(error[3])
