#!/bin/usr/env python3

# name:    test_appendfilename.py
# author:  nbehrnd@yahoo.com
# license: GPL v3, 2022.
# date:    2022-01-05 (YYYY-MM-DD)
# edit:    [2024-10-31 Thu]

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
import pytest
import sys
import subprocess

from pathlib import Path
from subprocess import getstatusoutput, getoutput

PROGRAM = str(Path("appendfilename") / "__init__.py")  # Cross-platform path

@pytest.mark.default
@pytest.mark.parametrize("arg1", ["test.txt", "2021-12-31_test.txt",
                                  "2021-12-31T18.48.22_test.txt"])
@pytest.mark.parametrize("arg2", ["-t book", "-t book_shelf"])#,
#                                  "--text book", "--text book_shelf"])
#@pytest.mark.parametrize("arg3", [" ", "!", "@", "#", "$", "%", "*", "_", "+",
@pytest.mark.parametrize("arg3", [" ", "!", "@", "#", "$", "%",       "_", "+",
                                  "=", "-"])
def test_pattern_s1(arg1, arg2, arg3):
    """Check addition just ahead the file extension.

    arg1   the test files to process
    arg2   the text string to be added
    arg3   the explicitly defined text separator (except [a-zA-Z])"""

    # extract the newly added text information:
    text_elements = arg2.split(" ")[1:]
    text = str(" ".join(text_elements))

    with open(arg1, mode="w") as newfile:
        newfile.write("This is a test file for test_appendfilename.")

    # Run the command with cross-platform Python executable and file paths
    result = subprocess.run(
        [sys.executable, PROGRAM, arg1, arg2, f"--separator={arg3}"],
        capture_output=True, text=True, check=True)

    new_filename = "".join([arg1[:-4], arg3, " ", text, str(".txt")])
    assert os.path.isfile(new_filename)

    # space cleaning
    os.remove(new_filename)