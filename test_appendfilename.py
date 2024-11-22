#!/bin/usr/env python3

# name:    test_appendfilename.py
# author:  nbehrnd@yahoo.com
# license: GPL v3, 2022.
# date:    2022-01-05 (YYYY-MM-DD)
# edit:    [2024-11-22 Fri]
#
"""Test pad for functions by appendfilename with pytest.

Initially written for Python 3.9.9 and pytest 6.2.4 and recently update
for Python 3.12.6/pytest 8.3.3, this script provides a programmatic check
of functions offered by appendfilename.  Deposit this script in the root
of the folder fetched and unzipped from PyPi or GitHub.  Create a virtual
environment for Python, e.g. by

```shell
python -m venv sup
```

In the activated virtual environment, resolve the dependencies - either by
`pip install pyreadline3 pytest`, or `pip install -r requirements.txt` -
and launch the tests by

```shell
python -m pytest
```

As a reminder, the following optional pytest flags may be useful to obtain
a report tailored to your needs:

- `-x` exit after the first failing test (reported by `E` instead of `.`)
- `-v` provide a more verbose output
- `-s` equally report the test criterion, e.g. the queried file name

Equally keep in mind you can constrain pytest tests.  Labels assigned are

- default:        test appendfilename's default string insertion
- prepend:        test appendfilename's optional -p/--prepend flag
- smart_prepend:  test appendfilename's optional --smart-prepend flag
"""

import re
import os
import shlex
import subprocess

from itertools import product

import pytest

PROGRAM = os.path.join("appendfilename", "__init__.py")

# The following section tests the applications default pattern where a
# string is added to the file name, just prior to the file's file
# extension.  The permutations of the arguments define 120 tests.

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
# Note: In Windows 10, the check with pytest and `*` as separator fails
# because it is not a permitted character in a file name there.  See
# <https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file>

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
    subprocess.run(full_command, text=True, check=True)

    # construct the new file name to be tested:
    if len(shlex.split(arg3)) == 0:
        separator = " "
    else:
        separator = shlex.split(arg3)[1]

    new_filename = "".join(
        [arg1[:-4], separator, shlex.split(arg2)[1], ".txt"])
    print(f"test criterion: {new_filename}")  # for an optional `pytest -s`

    # is the new file present?
    assert os.path.isfile(new_filename)

    # check if the OS can process the new file / space cleaning
    os.remove(new_filename)
    assert os.path.isfile(new_filename) is False

# The following section is about tests to prepend a user defined string
# and an adjustable separator to the original file name of the submitted
# file.  The permutation of the parameters defines 240 tests.


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
    subprocess.run(full_command, text=True, check=True)

    # construct the new file name to be tested:
    if len(shlex.split(arg3)) == 0:
        separator = " "
    else:
        separator = shlex.split(arg3)[1]

    new_filename = "".join([shlex.split(arg2)[1], separator, arg1])
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
    # "20211231_test.txt",  # by now `20211231_test.txt` -> 20211231_test ping.txt
    # "2021-12_test.txt",   # by now `2021-12_test.txt` -> `2021-12_test ping.txt`
    # "211231_test.txt"     # by now `211231_test.txt` -> `211231_test ping.txt`
]
arg2_values = [
    "-t book",
    "-t book_shelf",
    "--text book",
    "--text book_shelf"
]
arg3_values = [
    "",  # i.e. fall back to default single space
    # "--separator '!'",
    # "--separator '@'",
    # "--separator '#'",
    # "--separator '$'",
    # "--separator '%'",
    # "--separator '_'",
    # "--separator '+'",
    # "--separator '='",
    # "--separator '-'"
]
# Note: The check with pytest and `*` as separator in Windows 10 fails.
# Contrasting to Linux Debian 13, a `pytest` in Windows 10 revealed every
# of these special characters can not safely used as an additional separator.

# create the permutations:
test_cases = list(product(arg1_values, arg2_values, arg3_values))


@pytest.mark.smart_prepend
@pytest.mark.parametrize("arg1, arg2, arg3", test_cases)
def test_smart_prepend(arg1, arg2, arg3):
    """test the insertion of a new string just past the time stamp

    arg1   the test file to process, partly inspired by `date2name`
    arg2   the text string to be added
    arg3   the separator (at least in Windows 10, do not use `*`
    """
    timestamp = ""
    # timestamp_separator = ""
    old_filename_no_timestamp = ""

    # create a test file:
    with open(arg1, mode="w", encoding="utf-8") as newfile:
        newfile.write("this is a placeholder\n")

    # run `appendfilename` on this test file
    run_appendfilename = " ".join(
        ["python", PROGRAM, arg1, arg2, arg3, " --smart-prepend"])
    subprocess.run(run_appendfilename, shell=True, check=True)

    # construct the new file name to be testedt:
    old_filename = arg1

    # account for the implicit separator, i.e. the single space:
    if len(shlex.split(arg3)) == 0:
        separator = " "
    else:
        separator = shlex.split(arg3)[1]

    # Timestamps `date2name` provides can be either one of five formats
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

    patterns = [
        r"^\d{4}-[012]\d-[0-3]\dT[012]\d\.[0-5]\d\.[0-5]\d",
        r"^\d{4}-[012]\d-[0-3]\d",
        r"^\d{4}[012]\d[0-3]\d",
        r"^\d{4}-[012]\d",
        r"^\d{2}[012]\d[0-3]\d"
    ]

    for pattern in patterns:
        match = re.search(pattern, old_filename)
        if match:
            timestamp = re.findall(pattern, old_filename)[0]
            timestamp_separator = str(old_filename)[len(timestamp)]
            old_filename_no_timestamp = old_filename[len(timestamp) + 1:]

            print("\n\ntest of option smart-prepend:")  # `pytest -s` diagnosis
            print("old_filename:")
            print(old_filename)
            print("timestamp, timestamp_separator, old_filename_no_timestamp")
            print(timestamp)
            print(timestamp_separator)
            print(old_filename_no_timestamp)

            break

    new_filename = "".join([
        timestamp,  # timestamp_separator,
        separator, shlex.split(arg2)[1], separator,
        old_filename_no_timestamp
    ])

    # is the new file present?
    print("new_filename")  # optional check for `pytest -s`
    print(new_filename)
    assert os.path.isfile(new_filename)

    # check if the IS can process the new file / space cleaning
    os.remove(new_filename)
    assert os.path.isfile(new_filename) is False
