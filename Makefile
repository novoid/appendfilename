# GNU Make file for the automation of pytest for appendfilename
#
# While the test script is written for Python 3.9.2, it depends on
# your installation of pytest (and in case of Linux, the authors of
# your distribution) if pytest for Python 3 is invoked either by
# pytest, or pytest-3.  In some distributions, pytest actually may
# invoke pyest for legacy Python 2; the tests in test_date2name.py
# however are incompatible to this.
#
# Put this file like test_appendfilename.py in the root folder of
# appendfilename fetched from PyPi or GitHub.  Then run
#
# chmod +x *
# make ./Makefile
#
# to run the tests.  If you want pytest to exit the test sequence
# right after the first test failing, use the -x flag to the
# instructions on the CLI in addition to the verbosity flag to (-v).

# pytest -v test_appendfilename.py     # the pattern by pytest's manual
pytest-3 -v test_appendfilename.py   # the alternative pattern (e.g., Debian 12)
