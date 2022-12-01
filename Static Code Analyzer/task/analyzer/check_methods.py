import re
import ast


class LineByLineChecker:

    def __init__(self):
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

    def error_s001(self, line_no: int, line: str):  # 'Too long' e.c. >= 80
        if len(line) >= 80:
            self.errors.append([line_no,
                                'S001',
                                self.path,
                                f"{self.path}: Line {line_no}: S001 {self.codes['S001']}"])

    def error_s002(self, line_no: int, line: str):  # Indentation is not a multiple of four
        result = re.match("^( *)", line)
        if len(result.group()) % 4 != 0:  # or """if len(re.match('^ *', line)[0]) % 4 != 0:"""
            self.errors.append([line_no,
                                'S002',
                                self.path,
                                f"{self.path}: Line {line_no}: S002 {self.codes['S002']}"])

    def error_s003(self, line_no: int, line: str):  # Unnecessary semicolon after a statement
        if re.match(r".*\(.*\);.*", line) or re.match(" *[A-Za-z]*;", line):
            self.errors.append([line_no,
                                'S003',
                                self.path,
                                f"{self.path}: Line {line_no}: S003 {self.codes['S003']}"])

    def error_s004(self, line_no: int, line: str):  # Less than two spaces before inline comments
        if re.match(r'.*\S # .*', line):
            self.errors.append([line_no,
                                'S004',
                                self.path,
                                f"{self.path}: Line {line_no}: S004 {self.codes['S004']}"])

    def error_s005(self, line_no: int, line: str):  # TO_DO found (in comments only and case-insensitive)
        if re.match('.*#.*TODO.*', line, re.IGNORECASE):
            self.errors.append([line_no,
                                'S005',
                                self.path,
                                f"{self.path}: Line {line_no}: S005 {self.codes['S005']}"])

    def error_s006(self, line_no: int, line: str):  # More than two blank lines preceding a code line
        if line.strip() == '':
            self.blank_line_count += 1
            if self.blank_line_count > 2:
                self.errors.append([line_no + 1,
                                    'S006',
                                    self.path,
                                    f"{self.path}: Line {line_no + 1}: S006 {self.codes['S006']}"])
                self.blank_line_count = 0

    def error_s007(self, line_no: int, line: str):  # Too many spaces after construction_name (def or class)
        beginning_line = re.match(".*(class|def) {2,}", line)
        if beginning_line:
            name = beginning_line.groups()[0]
            self.errors.append([line_no,
                                'S007',
                                self.path,
                                f"{self.path}: Line {line_no}: S007 {self.codes['S007'].format(name)}"])

    def error_s008(self, line_no: int, line: str):  # Class name {} should be written in camelCase
        match = re.match("class ([a-z]+[a-z]*[A-Z]?[a-z]*)", line)
        if match:
            class_name = match.groups()[0]
            self.errors.append([line_no,
                                'S008',
                                self.path,
                                f"{self.path}: Line {line_no}: S008 {self.codes['S008'].format(class_name)}"])

    def error_s009(self, line_no: int, line: str):  # Function name {} should be written in snake_case
        # if not match right variants like __init__(), snake_case()
        if not re.match(".*def _{,2}?[a-z]*_?[a-z0-9]*_{,2}?\\(.*\\):$", line):
            match = re.match(".*def ([A-Z].*)\\(.*\\)", line)
            if match:
                def_name = match.groups()[0]
                self.errors.append([line_no,
                                    'S009',
                                    self.path,
                                    f"{self.path}: Line {line_no}: S009 {self.codes['S009'].format(def_name)}"])


class ASTChecker:

    def check_node_in_snake_case(self, obj):
        func = obj.__dict__
        lineno = func['lineno']
        arg_name = func['arg']
        if not re.match("^[a-z0-9_]*_?[a-z0-9]*$", arg_name):
            self.errors.append([lineno,
                                'S010',
                                self.path,
                                f"{self.path.lower()}: Line {lineno}: S010 {self.codes['S010'].format(arg_name)}"])

    def check_variable_in_snake_case(self, obj):
        if isinstance(obj, ast.Assign):
            for target in obj.targets:
                var_dict = target.__dict__
                try:
                    var_name = var_dict['id']
                    lineno = var_dict['lineno']
                except KeyError:
                    var_name = var_dict['value'].id + '.' + var_dict['attr']
                    lineno = var_dict['lineno']
                if not re.match("^[a-z0-9_]*\.?_?[a-z0-9]*$", var_name):
                    self.errors.append(
                        [lineno,
                         'S011',
                         self.path,
                         f"{self.path}: Line {lineno}: S011 {self.codes['S011'].format(var_name)}"])

    def check_default_argument_mutable(self, default):
        if not isinstance(default, ast.Constant):
            default_dict = default.__dict__
            lineno = default_dict['lineno']
            self.errors.append([lineno,
                                'S012',
                                self.path,
                                f"{self.path}: Line {lineno}: S012 {self.codes['S012']}"])
