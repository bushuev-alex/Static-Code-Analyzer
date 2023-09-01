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

To launch analysis you should print following string in CL:
* python3 code_analyser.py **path_to_folder_or_file** where **path_to_folder_or_file** is like:
  * '.' - default value (current folder)
  * /full/path/to/file.py
  * /full/path/to/folder