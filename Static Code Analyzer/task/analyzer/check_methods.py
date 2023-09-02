import re
import ast
from abc import ABC


class ParentChecker(ABC):

    def __init__(self):
        self.path = None
        self.errors = []
        self.blank_line_count = 0
        self.codes = {'S001': 'Too long',
                      'S002': 'Indentation is not a multiple of four',
                      'S003': 'Unnecessary semicolon after a statement',
                      'S004': 'Less than two spaces before inline comments',
                      'S005': 'TODO found',
                      'S006': 'More than two blank lines preceding a code line',
                      'S007': "Too many spaces after '{}'",
                      'S008': "Class name '{}' should be written in CamelCase",
                      'S009': 'Function name {} should be written in snake_case',
                      'S010': "Argument name {} should be written in snake_case",
                      'S011': "Variable {} should be written in snake_case",
                      'S012': "Default argument value is mutable"}


class LineByLineChecker(ParentChecker):

    def error_s001(self, line_no: int, line: str, path: str) -> bool:  # 'Too long' e.c. >= 80
        if len(line) >= 80:
            self.errors.append((line_no,
                                'S001',
                                path,
                                f"{path}: Line {line_no}: S001 {self.codes['S001']}"))
            return True
        return False

    def error_s002(self, line_no: int, line: str, path: str) -> bool:  # Indentation is not a multiple of four
        result = re.match("^( *)", line)
        if len(result.group()) % 4 != 0:  # or """if len(re.match('^ *', line)[0]) % 4 != 0:"""
            self.errors.append((line_no,
                                'S002',
                                path,
                                f"{path}: Line {line_no}: S002 {self.codes['S002']}"))
            return True
        return False

    def error_s003(self, line_no: int, line: str, path: str) -> bool:  # Unnecessary semicolon after a statement
        if re.match(r".*\(.*\);.*", line) or re.match(" *[A-Za-z]*;", line):
            self.errors.append((line_no,
                                'S003',
                                path,
                                f"{path}: Line {line_no}: S003 {self.codes['S003']}"))
            return True
        return False

    def error_s004(self, line_no: int, line: str, path: str) -> bool:  # Less than two spaces before inline comments
        if re.match(r'.*\S # .*', line):
            self.errors.append((line_no,
                                'S004',
                                path,
                                f"{path}: Line {line_no}: S004 {self.codes['S004']}"))
            return True
        return False

    def error_s005(self, line_no: int, line: str,
                   path: str) -> bool:  # TO_DO found (in comments only and case-insensitive)
        if re.match('.*#.*TODO.*', line, re.IGNORECASE):
            self.errors.append((line_no,
                                'S005',
                                path,
                                f"{path}: Line {line_no}: S005 {self.codes['S005']}"))
            return True
        return False

    def error_s006(self, line_no: int, line: str, path: str) -> bool:  # More than two blank lines preceding a code line
        if line.strip() == '':
            self.blank_line_count += 1
        if self.blank_line_count > 2:
            self.errors.append((line_no + 1,
                                'S006',
                                path,
                                f"{path}: Line {line_no + 1}: S006 {self.codes['S006']}"))
            self.blank_line_count = 0
            return True
        return False

    def error_s007(self, line_no: int, line: str,
                   path: str) -> bool:  # Too many spaces after construction_name (def or class)
        beginning_line = re.match(".*(class|def) {2,}", line)
        if beginning_line:
            name = beginning_line.groups()[0]
            self.errors.append((line_no,
                                'S007',
                                path,
                                f"{path}: Line {line_no}: S007 {self.codes['S007'].format(name)}"))
            return True
        return False

    def error_s008(self, line_no: int, line: str, path: str) -> bool:  # Class name {} should be written in camelCase
        match = re.match("class ([a-z]+[a-z]*[A-Z]?[a-z]*)", line)
        if match:
            class_name = match.groups()[0]
            self.errors.append((line_no,
                                'S008',
                                path,
                                f"{path}: Line {line_no}: S008 {self.codes['S008'].format(class_name)}"))
            return True
        return False

    def error_s009(self, line_no: int, line: str,
                   path: str) -> bool:  # Function name {} should be written in snake_case
        # if not match right variants like __init__(), snake_case()
        if not re.match(".*def _{,2}?[a-z]*_?[a-z0-9]*_{,2}?\\(.*\\):$", line):
            match = re.match(".*def ([A-Z].*)\\(.*\\)", line)
            if match:
                def_name = match.groups()[0]
                self.errors.append((line_no,
                                    'S009',
                                    path,
                                    f"{path}: Line {line_no}: S009 {self.codes['S009'].format(def_name)}"))
                return True
            return False


class ASTChecker(ParentChecker):

    def check_node_in_snake_case(self, obj, path: str) -> bool:
        lineno = obj.lineno
        arg_name = obj.arg
        if not re.match("^[a-z0-9_]*_?[a-z0-9]*$", arg_name):
            self.errors.append((lineno,
                                'S010',
                                path,
                                f"{path.lower()}: Line {lineno}: S010 {self.codes['S010'].format(arg_name)}"))
            return True
        return False

    def check_variable_in_snake_case(self, obj, path: str) -> bool:
        if isinstance(obj, ast.Assign):
            for target in obj.targets:
                var_dict = target.__dict__
                var_name = var_dict.get('id')
                lineno = var_dict.get('lineno')
                if not (var_name and lineno):
                    var_name_id = var_dict.get('value').__dict__.get('id')
                    var_name_attr = var_dict.get('attr')
                    lineno = var_dict.get('lineno')
                    if not (var_name_id and var_name_attr and lineno):
                        var_name_id = var_dict.get('value').__dict__.get('value').__dict__.get('id')
                        var_name_attr = var_dict.get('value').__dict__.get('attr')
                        lineno = var_dict.get('value').__dict__.get('lineno')
                    var_name = '.'.join((var_name_id, var_name_attr))
                if not re.match("^[a-z0-9_]*\.?_?[a-z0-9_]*$", var_name):
                    self.errors.append((lineno,
                                        'S011',
                                        path,
                                        f"{path}: Line {lineno}: S011 {self.codes['S011'].format(var_name)}"))
            return True
        return False

    def check_default_argument_mutable(self, default, path: str) -> bool:
        if not isinstance(default, ast.Constant):
            lineno = default.lineno
            self.errors.append((lineno,
                                'S012',
                                path,
                                f"{path}: Line {lineno}: S012 {self.codes['S012']}"))
            return True
        return False
