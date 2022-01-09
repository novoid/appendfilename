#!/bin/usr/env python3

# name:    test_appendfilename.py
# author:  nbehrnd@yahoo.com
# license: GPL v3, 2022.
# date:    2022-01-05 (YYYY-MM-DD)
# edit:    2022-01-09 (YYYY-MM-DD)
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
from subprocess import getstatusoutput, getoutput

import pytest

PROGRAM = str("./appendfilename/__init__.py")

@pytest.mark.default
@pytest.mark.parametrize("arg1", ["test.txt", "2021-12-31_test.txt",
                                  "2021-12-31T18.48.22_test.txt",
                                  "20211231_test.txt", "2012-12_test.txt",
                                  "211231_test.txt"])
@pytest.mark.parametrize("arg2", ["-t book", "-t book_shelf",
                                  "--text book", "--text book_shelf"])
@pytest.mark.parametrize("arg3", [" ", "!", "@", "#", "$", "%", "*", "_", "+",
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

    test = getoutput(f"python3 {PROGRAM} {arg1} {arg2} --separator={arg3}")

    new_filename = "".join([arg1[:-4], arg3, text, str(".txt")])
    assert os.path.isfile(new_filename)

    os.remove(new_filename)
    assert os.path.isfile(new_filename) is False

@pytest.mark.prepend
@pytest.mark.parametrize("arg1", ["test.txt", "2021-12-31_test.txt",
                                  "2021-12-31T18.48.22_test.txt",
                                  "20211231_test.txt", "2012-12_test.txt",
                                  "211231_test.txt"])
@pytest.mark.parametrize("arg2", ["-t book", "-t book_shelf",
                                  "--text book", "--text book_shelf"])
@pytest.mark.parametrize("arg3", [" ", "!", "@", "#", "$", "%", "*", "_", "+",
                                  "=", "-"])
@pytest.mark.parametrize("arg4", ["-p", "--prepend"])
def test_pattern_s2(arg1, arg2, arg3, arg4):
    """Check addition just ahead the file extension.

    arg1   the test files to process
    arg2   the text string to be added
    arg3   the explicitly defined text separator (except [a-zA-Z])
    arg4   use either of two forms of the prepend flag."""

    # extract the newly added text information:
    text_elements = arg2.split(" ")[1:]
    text = str(" ".join(text_elements))

    with open(arg1, mode="w") as newfile:
        newfile.write("This is a test file for test_appendfilename.")

    test = getoutput(f"python3 {PROGRAM} {arg1} {arg2} --separator={arg3} {arg4}")

    new_filename = "".join([text, arg3, arg1])
    assert os.path.isfile(new_filename)

    os.remove(new_filename)
    assert os.path.isfile(new_filename) is False

@pytest.mark.smart
@pytest.mark.parametrize("arg1", ["test.txt", "2021-12-31_test.txt",
                                  "2021-12-31T18.48.22_test.txt"])
@pytest.mark.parametrize("arg2", ["-t book", "-t book_shelf",
                                  "--text book", "--text book_shelf"])
@pytest.mark.parametrize("arg3", [" " , "#", "!", "@", "#", "$", "%", "*", "_", "+",
                                  "=", "-"])
def test_pattern_s3_02(arg1, arg2, arg3):
    """Check addition retaining time stamp on leading position.

    arg1   the test files to process
    arg2   the text string to be added
    arg3   the explicitly defined text separator (except [a-zA-Z])."""

    # extract the newly added text information:
    text_elements = arg2.split(" ")[1:]
    text = str(" ".join(text_elements))

    with open(arg1, mode="w") as newfile:
        newfile.write("This is a test file for test_appendfilename.")

    test = getoutput(f"python3 {PROGRAM} {arg1} {arg2} --separator={arg3} --smart-prepend")
    
    # analysis section:
    old_filename = str(arg1)

    if (re.search("^\d{4}-[012]\d-[0-3]\d_", old_filename) or
        re.search('^\d{4}-[012]\d-[0-3]\dT[012]\d\.[0-5]\d\.[0-5]\d_', old_filename)):

        if re.search("^\d{4}-\d{2}-\d{2}_", old_filename):
            # if (running date2name in default mode) then .true.
            time_stamp = old_filename[:10]
            time_stamp_separator = old_filename[10]
            file_extension = old_filename.split(".")[-1]
            old_filename_no_timestamp = old_filename[11:]
            
        elif re.search('^\d{4}-\d{2}-\d{2}T\d{2}\.\d{2}\.\d{2}_', old_filename):
            # if (running date2name --withtime) then .true.
            time_stamp = old_filename[:19]
            time_stamp_separator = old_filename[19]
            file_extension = old_filename.split(".")[-1]
            old_filename_no_timestamp = old_filename[20:]
            
        stem_elements = old_filename_no_timestamp.split(".")[:-1]
        stem = ".".join(stem_elements)

        new_filename = "".join([time_stamp, arg3, text, arg3, stem, str("."), file_extension])
        assert os.path.isfile(new_filename)

        os.remove(new_filename)
        assert os.path.isfile(new_filename) is False

    else:
        # within the scope set, a file which did not pass date2name earlier
        new_filename = "".join([text, arg3, old_filename])
        assert os.path.isfile(new_filename)

        os.remove(new_filename)
        assert os.path.isfile(new_filename) is False
