#!/bin/usr/env python3

# name:    test_appendfilename.py
# author:  nbehrnd@yahoo.com
# license: GPL v3, 2022.
# date:    2022-01-05 (YYYY-MM-DD)
# edit:    [2024-11-05 Tue]
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

@pytest.mark.default
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

@pytest.mark.prepend
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

# This section tests the insertion of a string into the file's file name
# just after the file's time or date stamp as provided `date2name`.

arg1_values = [
    "2021-12-31T18.48.22_test.txt",
    "2021-12-31_test.txt",
#    "20211231_test.txt",  # by now `20211231_test.txt` -> 20211231_test ping.txt
#    "2021-12_test.txt",   # by now `2021-12_test.txt` -> `2021-12_test ping.txt`
#    "211231_test.txt"     # by now `211231_test.txt` -> `211231_test ping.txt`
]
arg2_values = [
    "-t book",
    "-t book_shelf",
    "--text book",
    "--text book_shelf"
]
arg3_values = [
    "",  # i.e. fall back to default single space
#    "--separator '!'",
#    "--separator '@'",
#    "--separator '#'",
#    "--separator '$'",
#    "--separator '%'",
#    "--separator '_'",
#    "--separator '+'",
#    "--separator '='",
#    "--separator '-'"
]
# Note: The check with pytest and `*` as separator in Windows 10 fails.
# Contrasting to Linux Debian 13, a `pytest` in Windows 10 revealed every
# of these special characters can not safely used as an additional separator.

# create the permutations:
test_cases = list(product(arg1_values, arg2_values, arg3_values))

@pytest.mark.smart
@pytest.mark.parametrize("arg1, arg2, arg3", test_cases)
def test_smart_prepend(arg1, arg2, arg3):
    """test the insertion of a new string just past the time stamp

    arg1   the test file to process, partly inspired by `date2name`
    arg2   the text string to be added
    arg3   the separator (at least in Windows 10, do not use `*`
    """
    time_stamp = ""
    time_stamp_separator = ""
    old_filename_no_timestamp = ""

    # create a test file:
    with open(arg1, mode="w", encoding="utf-8") as newfile:
        newfile.write("this is a placeholder\n")

    #run `appendfilename` on this test file
    run_appendfilename = " ".join(
        ["python", PROGRAM, arg1, arg2, arg3, " --smart-prepend"])
    subprocess.run(run_appendfilename, shell=True, check = True)

    # construct the new file name to be testedt:
    old_filename = arg1

    # account for the implicit separator, i.e. the single space:
    if len(shlex.split(arg3)) == 0:
        separator = " "
    else:
        separator = shlex.split(arg3)[1]

    # Time stamps `date2name` provides can be either one of five formats
    #
    # YYYY-MM-DDTHH.MM.SS   `--withtime`
    # YYYY-MM-DD            default
    # YYYYMMDD              `--compact`
    # YYYY-MM               `--month`
    # YYMMDD                `--short`

    # Currently, one observes two patterns by `appendfilename`: one which
    # substitutes the separator by `date2name`, the other which retains it.
    # Note patterns `compact`, `month`, and `short`, currently append the
    # additional string rather than smartly prepend after the date stamp --
    # for now, these three are not tested.  Equally see discussions 15 and 16,
    # https://github.com/novoid/appendfilename/issues/15
    # https://github.com/novoid/appendfilename/issues/16

    # pattern `--with-time`
    if re.search(r"^\d{4}-[012]\d-[0-3]\dT[012]\d\.[0-5]\d\.[0-5]\d", old_filename):
        time_stamp = old_filename[:19]
        time_stamp_separator = old_filename[19]
        old_filename_no_timestamp = old_filename[20:]

    # default pattern
    elif re.search(r"^\d{4}-[012]\d-[0-3]\d", old_filename):
        time_stamp = old_filename[:10]
        time_stamp_separator = old_filename[10]
        old_filename_no_timestamp = old_filename[11:]

    # pattern `--compact`  # currently fails
    elif re.search(r"^\d{4}[012]\d[0-3]\d", old_filename):
        time_stamp = old_filename[:8]
        time_stamp_separator = old_filename[8]
        old_filename_no_timestamp = old_filename[9:]

    # pattern `--month`  # currently fails
    elif re.search(r"^\d{4}-[012]\d", old_filename):
        time_stamp = old_filename[:7]
        time_stamp_separator = old_filename[7]
        old_filename_no_timestamp = old_filename[8:]

    # pattern `--short`  # currently fails
    elif re.search(r"^\d{4}[012]\d[012]\d", old_filename):
        time_stamp = old_filename[:6]
        time_stamp_separator = old_filename[6]
        old_filename_no_timestamp = old_filename[7:]

    new_filename = "".join([time_stamp, #time_stamp_separator,
        separator, shlex.split(arg2)[1], separator,
        old_filename_no_timestamp ])

    # is the new file present?
    print("\nnew_filename")  # optional check for `pytest -s`
    print(new_filename)
    assert os.path.isfile(new_filename)

    # check if the IS can process the new file / space cleaning
    os.remove(new_filename)
    assert os.path.isfile(new_filename) is False
