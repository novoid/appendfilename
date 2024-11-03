#!/bin/usr/env python3

# name:    test_appendfilename.py
# author:  nbehrnd@yahoo.com
# license: GPL v3, 2022.
# date:    2022-01-05 (YYYY-MM-DD)
# edit:    [2024-11-03 Sun]
#
"""Test pad for functions by appendfilename with pytest.

Written for Python 3.9.9 and pytest 6.2.4 for Python 3 as provided by
Linux Debian 12/bookworm, branch testing, this is a programmatic check
of functions offered by appendfilename.  Deposit this script in the root of
the folder fetched and unzipped from PyPi or GitHub.  If your system
includes both legacy Python 2 and Python 3, pytest for Python 3 likely
is named pytest-3; otherwise only pytest.  Thus, adjust your input on
the CLI accordingly when running either one of

pytest -v test_appendfilename.py
pytest-3 -v test_appendfilename.py

These instruction initiate a verbose testing (flag -v) reported back to the
CLI.re will be a verbose report to the CLI The script either stops when one of
the tests fail (flag -x), or after completion of the test sequence.  In both
cases, the progress of the ongoing tests is reported to the CLI (flag -v)."""

import re
import os
import shlex
import sys
import subprocess

from itertools import product

import pytest

PROGRAM = os.path.join("appendfilename", "__init__.py")  # Cross-platform path

# The following section tests the applications default pattern where a string
# is added to the file name, just prior to the file's file extension.

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
