#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2013-05-16 22:52:45 vk>

## TODO:
## * fix parts marked with «FIXXME»



## ===================================================================== ##
##  You might not want to modify anything below this line if you do not  ##
##  know, what you are doing :-)                                         ##
## ===================================================================== ##

## NOTE: in case of issues, check iCalendar files using: http://icalvalid.cloudapp.net/

import re
import sys
import os
import time
import logging
from optparse import OptionParser

## debugging:   for setting a breakpoint:  pdb.set_trace()
import pdb

PROG_VERSION_NUMBER = u"0.1"
PROG_VERSION_DATE = u"2013-05-16"
INVOCATION_TIME = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
FILENAME_TAG_SEPARATOR = u' -- ' ## between file name and (optional) list of tags
BETWEEN_TAG_SEPARATOR = u' '  ## between tags (not that relevant in this tool)
TEXT_SEPARATOR = u' '  ## between old file name and inserted text

USAGE = u"\n\
    " + sys.argv[0] + u" [<options>] <list of files>\n\
\n\
This tool inserts text between the old file name and optional tags or file extension.\n\
\n\
\n\
Text within file names is placed between the actual file name and\n\
the file extension or (if found) between the actual file namd and\n\
a set of tags separated with \"" + FILENAME_TAG_SEPARATOR + "\".\n\
  Update for the Boss " + TEXT_SEPARATOR + "<NEW TEXT HERE>.pptx\n\
  2013-05-16T15.31.42 Error message" + TEXT_SEPARATOR + "<NEW TEXT HERE>" \
    + FILENAME_TAG_SEPARATOR + "screenshot" + BETWEEN_TAG_SEPARATOR + "projectB.png\n\
\n\
Example usages:\n\
  " + sys.argv[0] + u" --text=\"of projectA\" \"the presentation.pptx\"\n\
      ... results in \"the presentation" + TEXT_SEPARATOR + "of projectA.pptx\"\n\
  " + sys.argv[0] + u" \"2013-05-09T16.17_img_00042 -- fun.jpeg\"\n\
      ... with interactive input of \"Peter\" results in:\n\
          \"2013-05-09T16.17_img_00042" + TEXT_SEPARATOR + "Peter -- fun.jpeg\"\n\
\n\
\n\
:copyright: (c) 2013 by Karl Voit <tools@Karl-Voit.at>\n\
:license: GPL v3 or any later version\n\
:URL: https://github.com/novoid/filetag\n\
:bugreports: via github or <tools@Karl-Voit.at>\n\
:version: " + PROG_VERSION_NUMBER + " from " + PROG_VERSION_DATE + "\n"


## file names containing optional tags matches following regular expression
FILE_WITH_EXTENSION_REGEX = re.compile("(.*?)(( -- .*)?\.\w+?)$")
FILE_WITH_EXTENSION_FILENAME_INDEX = 1
FILE_WITH_EXTENSION_TAGS_AND_EXT_INDEX = 2

#1 TEXT#2



parser = OptionParser(usage=USAGE)

parser.add_option("-t", "--text", dest="text",
                  help="the text to add to the file name")

parser.add_option("-s", "--dryrun", dest="dryrun", action="store_true",
        help="enable dryrun mode: just simulate what would happen, do not modify file(s)")

parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                  help="enable verbose mode")

parser.add_option("-q", "--quiet", dest="quiet", action="store_true",
                  help="enable quiet mode")

parser.add_option("--version", dest="version", action="store_true",
                  help="display version and exit")

(options, args) = parser.parse_args()


def handle_logging():
    """Log handling and configuration"""

    if options.verbose:
        FORMAT = "%(levelname)-8s %(asctime)-15s %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    elif options.quiet:
        FORMAT = "%(levelname)-8s %(message)s"
        logging.basicConfig(level=logging.ERROR, format=FORMAT)
    else:
        FORMAT = "%(levelname)-8s %(message)s"
        logging.basicConfig(level=logging.INFO, format=FORMAT)


def error_exit(errorcode, text):
    """exits with return value of errorcode and prints to stderr"""

    sys.stdout.flush()
    logging.error(text)

    sys.exit(errorcode)


def handle_file(filename, text, dryrun):
    """
    @param filename: one file name
    @param text: string that shall be added to file name(s)
    @param dryrun: boolean which defines if files should be changed (False) or not (True)
    @param return: error value
    """

    if os.path.isdir(filename):
        logging.warning("Skipping directory \"%s\" because this tool only processes file names." % filename)
        return
    elif not os.path.isfile(filename):
        logging.error("Skipping \"%s\" because this tool only processes existing file names." % filename)
        return

    components = re.match(FILE_WITH_EXTENSION_REGEX, filename)
    old_filename = components.group(FILE_WITH_EXTENSION_FILENAME_INDEX)
    tags_with_extension = components.group(FILE_WITH_EXTENSION_TAGS_AND_EXT_INDEX)

    new_filename = old_filename + TEXT_SEPARATOR + text + tags_with_extension

    if dryrun:
        logging.info(u" ")
        logging.info(u" renaming \"%s\"" % filename)
        logging.info(u"      ⤷   \"%s\"" % (new_filename))
    else:
        logging.debug(u" renaming \"%s\"" % filename)
        logging.debug(u"      ⤷   \"%s\"" % (new_filename))
        os.rename(filename, new_filename)


def main():
    """Main function"""

    if options.version:
        print os.path.basename(sys.argv[0]) + " version " + PROG_VERSION_NUMBER + \
            " from " + PROG_VERSION_DATE
        sys.exit(0)

    handle_logging()

    if options.verbose and options.quiet:
        error_exit(1, "Options \"--verbose\" and \"--quiet\" found. " +
                   "This does not make any sense, you silly fool :-)")

    text = options.text

    if not text:

        logging.debug("interactive mode: asking for text ...")
        logging.info("Interactive mode: add text to file name ...")

        print "Please enter text:               (abort with Ctrl-C)"
        text = sys.stdin.readline().strip()

        logging.info("adding text \"%s\" ..." % text)
            
    logging.debug("text found: [%s]" % text)

    logging.debug("extracting list of files ...")
    logging.debug("len(args) [%s]" % str(len(args)))
    if len(args)<1:
        error_exit(2, "Please add at least one file name as argument")
    files = args
    logging.debug("%s filenames found: [%s]" % (str(len(files)), '], ['.join(files)))

    logging.debug("iterate over files ...")
    for filename in files:
        handle_file(filename, text, options.dryrun)

    logging.debug("successfully finished.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:

        logging.info("Received KeyboardInterrupt")

## END OF FILE #################################################################

#end
