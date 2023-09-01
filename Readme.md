# General info
To make sure your Python code is beautiful and consistently formatted, you should follow the PEP8 specification and 
best practices recommended by the Python community. This is not always easy, especially for beginners. 

Luckily, there are special tools called static code analyzers (pylint, flake8, and others) that automatically check 
that your code meets all the standards and recommendations. \
These tools don't execute your code but just analyze it 
and output all the issues they find.


In this project, you will create a small static analyzer tool that finds some common stylistic mistakes in Python code. 
This way, you will familiarize yourself with the concept of static code analysis and improve your Python skills along the way.

## How to 
This is CLI (command line interface) analyser. You can analyse files and folders with it. 

To launch analysis you should input string with following values in CL:
* python3 code_analyser.py path=**path_to_folder_or_file** \
where **path_to_folder_or_file** is like:
  * '.' - default value (current folder)
  * /full/path/to/file.py
  * /full/path/to/folder


## Output information about errors
Information about errors looks like:
* file_name.py:  line_number:  error_code:  error_description

Analyser gives information about 12 errors:
* 'S001': 'Too long'
* 'S002': 'Indentation is not a multiple of four'
* 'S003': 'Unnecessary semicolon after a statement'
* 'S004': 'Less than two spaces before inline comments'
* 'S005': 'TODO found'
* 'S006': 'More than two blank lines preceding a code line'
* 'S007': "Too many spaces after '{}'"
* 'S008': "Class name '{}' should be written in CamelCase"
* 'S009': 'Function name {} should be written in snake_case'
* 'S010': "Argument name {} should be written in snake_case"
* 'S011': "Variable {} should be written in snake_case"
* 'S012': "Default argument value is mutable"
