#!/bin/usr/env python3

# name:    test_appendfilename.py
# author:  nbehrnd@yahoo.com
# license: GPL v3, 2022.
# date:    2022-01-05 (YYYY-MM-DD)
# edit:    [2024-11-03 Sun]
#
"""Test pad for functions by appendfilename with pytest.

Initially written for Python 3.9.9 and pytest 6.2.4 and recently update
for Python 3.12.6/pytest 8.3.3, this script provides a programmatic check
of functions offered by appendfilename.  Deposit this script in the root of
the folder fetched and unzipped from PyPi or GitHub.  Create a virtual
environment for Python, e.g. by

```shell
python -m venv sup
```

In the activated virtual environment, ensure the dependencies are met -
either by `pip install pyreadline3 pytest`, or `pip install -r requirements.txt`
- and launch the tests by

```shell
python -m pytest
```

As a reminder, the following optional pytest flags may be useful to obtain
a report tailored to your needs:

- `-x` exits right after the first failing test (reported by `E` instead of `.`)
- `-v` provide a more verbose output
- `-s` equally report the test criterion, e.g. the queried file name
"""

import re
import os
import shlex
import sys
import subprocess

from itertools import product

import pytest

PROGRAM = os.path.join("appendfilename", "__init__.py")  # Cross-platform path

# The following section tests the applications default pattern where a string
# is added to the file name, just prior to the file's file extension.  The
# permutation of the three arguments and their levels defines 120 tests.

arg1_values = [
    "test.txt", "2021-12-31_test.txt", "2021-12-31T18.48.22_test.txt"
]
arg2_values = [
    "-t book", "-t book_shelf", "--text book", "--text book_shelf"
]
arg3_values = [
    "",  # i.e. fall back to default single space
    "--separator '!'",
    "--separator '@'",
    "--separator '#'",
    "--separator '$'",
    "--separator '%'",
    "--separator '_'",
    "--separator '+'",
    "--separator '='",
    "--separator '-'"
]
# Note: The check with pytest and `*` as separator in Windows 10 fails.

# create the permutations:
test_cases = list(product(arg1_values, arg2_values, arg3_values))

@pytest.mark.parametrize("arg1, arg2, arg3", test_cases)
def test_append(arg1, arg2, arg3):
    """Test default which appends a string just prior file extension

    arg1   the test file to process, partly inspired by `date2name`
    arg2   the text string to be added
    arg3   the separator (at least in Windows 10, do not use `*`)"""

    # create a test file:
    with open(arg1, mode="w", encoding="utf-8") as newfile:
        newfile.write("This is a place holder.\n")

    # run the test to be tested:
    full_command = ["python", PROGRAM, arg1
                    ] + shlex.split(arg2) + shlex.split(arg3)
    subprocess.run(full_command, text = True, check = True)

    # construct the new file name to be tested:
    if len(shlex.split(arg3)) == 0:
        separator = " "
    else:
        separator = shlex.split(arg3)[1]

    new_filename = "".join(
        [ arg1[:-4], separator,
          shlex.split(arg2)[1], ".txt" ])
    print(f"test criterion: {new_filename}")  # visible by optional `pytest -s`

    # is the new file present?
    assert os.path.isfile(new_filename)

    # check if the OS can process the new file / space cleaning
    os.remove(new_filename)
    assert os.path.isfile(new_filename) is False

# The following section is about tests to prepend a user defined string and
# an adjustable separator to the original file name of the file submitted.  By
# permutation of the parameter's levels, this defines 240 tests.

arg1_values = [
    "test.txt", "2021-12-31_test.txt", "2021-12-31T18.48.22_test.txt"
]
arg2_values = [
    "-t book", "-t book_shelf", "--text book", "--text book_shelf"
]
arg3_values = [
    "",  # i.e. fall back to default single space
    "--separator '!'",
    "--separator '@'",
    "--separator '#'",
    "--separator '$'",
    "--separator '%'",
    "--separator '_'",
    "--separator '+'",
    "--separator '='",
    "--separator '-'"
]
# Note: The check with pytest and `*` as separator in Windows 10 fails.

arg4_values = [
    "-p", "--prepend"
]

# create the permutations:
test_cases = list(product(arg1_values, arg2_values, arg3_values, arg4_values))

@pytest.mark.parametrize("arg1, arg2, arg3, arg4", test_cases)
def test_prepend(arg1, arg2, arg3, arg4):
    """test to prepend a string to the original file name

    arg1   the test file to process, partly inspired by `date2name`
    arg2   the text string to be added
    arg3   the separator (at least in Windows 10, do not use `*`)
    arg4   either short of long form to introduce the string as leading """

    # create a test file:
    with open(arg1, mode="w", encoding="utf-8") as newfile:
        newfile.write("This is a place holder.\n")

    # run the test to be tested:
    full_command = [
        "python", PROGRAM, arg1
        ] + shlex.split(arg2) + shlex.split(arg3) + shlex.split(arg4)
    subprocess.run(full_command, text = True, check = True)

    # construct the new file name to be tested:
    if len(shlex.split(arg3)) == 0:
        separator = " "
    else:
        separator = shlex.split(arg3)[1]

    new_filename = "".join( [ shlex.split(arg2)[1], separator, arg1 ] )
    print(f"test criterion: {new_filename}")  # visible by optional `pytest -s`

    # is the new file present?
    assert os.path.isfile(new_filename)

    # check if the OS can process the new file / space cleaning
    os.remove(new_filename)
    assert os.path.isfile(new_filename) is False
