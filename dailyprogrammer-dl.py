#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""dailyprogrammer-dl

Usage:
  dailyprogrammer-dl [options] <challengeurl>
  dailyprogrammer-dl -h | --help
  dailyprogrammer-dl --version

Automates the initial setup of a http://www.reddit.com/r/dailyprogrammer/
project

Examples:
  dailyprogrammer-dl https://www.reddit.com/r/dailyprogrammer/comments/3ggli3/20150810_challenge_227_easy_square_spirals/

Options:
  -q, --quiet           Print less text.
  -v, --verbose         Print more text.
  -h, --help            Show help.
  --version             Show version.
"""

from docopt import docopt
#TODO.. could use something more lightweight (requests/bs4) instead of robobrowser as login is no longer required?
from robobrowser import RoboBrowser
import logging
import re
import shutil
import os
import html2text


__appname__ = "dailyprogrammer-dl"
__author__  = "David Maranhao"
__license__ = "MIT"
__version__ = "0.1.0" # MAJOR.MINOR.PATCH | http://semver.org


def main():
    args = docopt(__doc__, version="dailyprogrammer-dl v{}".format(__version__))

    # Configure logging
    logLevel = logging.INFO #default
    if args['--verbose']:
        logLevel = logging.DEBUG
    elif args['--quiet']:
        logLevel = logging.ERROR

    logging.basicConfig(format='%(levelname)s: %(message)s', level=logLevel)
    logging.debug(args)

    # Process command line arguments
    challengeURL = args['<challengeurl>']

    # Parse project page for title and description
    logging.info("Parsing daily challenge: {}".format(challengeURL))
    browser = RoboBrowser(history=True, parser='html.parser')
    browser.session.headers['User-Agent'] = "dailyprogrammer-dl v{} by /u/zod77".format(__version__)
    browser.open(challengeURL)
    title = browser.find('a',class_='title').string
    description = browser.find_all('div',class_="md")
    description = description[1]
    descriptionHTML = "".join(str(t) for t in description.contents) # remove outer <div>

    projectName = generateProjectName(title)

    # Init project skeleton
    logging.info("Generating project")
    projectPath = os.path.abspath(projectName)
    os.mkdir(projectPath)

    # Write out project files
    pyTemplate = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),"boilerplate.txt"))
    shutil.copy(pyTemplate, os.path.join(projectPath,"{}.py".format(projectName)))

    # Generate README.md
    h = html2text.HTML2Text()
    descriptionMD = h.handle(descriptionHTML)
    readme = os.path.join(projectPath,"README.md")
    with open(readme, "w") as f:
        f.write(descriptionMD)

    return


def prependText( s, fn ):
    with open(fn,'r') as f:
        t = f.read()
    with open(fn,'w') as f:
        f.write(s)
        f.write(t)


def generateProjectName( s ):
    m = re.search("Challenge #(\d+) \[(\w+)\] (.+)",s)
    if m:
        name = "{}{}-{}".format(m.group(1),m.group(2)[0].upper(),m.group(3).lower())
        name = re.sub("\s","-",name)        # convert whitespace to dashes
        name = re.sub("[^\w\s-]","",name)   # strip punctuation
    else:
        name = s

    return name


if __name__ == "__main__":
    main()



