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
from robobrowser import RoboBrowser
import urllib
import logging
import re
import shutil
import os
import glob
import shlex
import subprocess

import html2text
from bs4 import BeautifulSoup


VERSION="0.1.0" # MAJOR.MINOR.PATCH | http://semver.org

def main():
    args = docopt(__doc__, version="dailyprogrammer-dl v{}".format(VERSION))

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
    #browser = RoboBrowser()
    #browser.open(challengeURL)
    #title = browser.find('a',class_='title').string
    #description = browser.find('div',class_="md")

    soup = BeautifulSoup(open('test.html'))
    title = soup.find('a',class_='title').string
    description = soup.find_all('div',class_="md")
    description = description[1]
    descriptionHTML = "".join(str(t) for t in description.contents) # remove outer <div>

    print(title)
    print(descriptionHTML)
    #print(description)
    #print(description)
    #print(description)

    projectName = generateProjectName(title)
    print(projectName)

    h = html2text.HTML2Text()
    descriptionMD = h.handle(descriptionHTML)
    print(descriptionMD)

    # Init project skeleton
    logging.info("Generating project")
    projectPath = os.path.abspath(projectName)
    os.mkdir(projectPath)

    # Write out project files
    pyTemplate = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),"boilerplate.txt"))
    shutil.copy(pyTemplate, os.path.join(projectPath,"{}.py".format(projectName)))

    readme = os.path.join(projectPath,"README.md")
    with open(readme, "w") as f:
        f.write(descriptionMD)

    ## Initialize git repo
    #shellCommand("git init",cwd=projectPath)
    #shellCommand("git add {}-src.txt".format(projectName),cwd=projectPath)
    #shellCommand('git commit -m "dailyprogrammer-dl: Initial version"',cwd=projectPath)
    #
    ## Convert to UTF-8
    #shellCommand("recode ISO-8859-1..UTF-8 {}".format(os.path.abspath("{}/{}-src.txt".format(projectName,projectName))))
    #prependText('', projectFilePath) # convert to native line endings
    #shellCommand('git commit -am "dailyprogrammer-dl: Convert to UTF-8, native line endings"',cwd=projectPath)
    #
    ## Add title
    #titleTxt = ".dt {}, by {}—A Project Gutenberg eBook\n".format(title,author)
    #prependText(titleTxt, projectFilePath)
    #shellCommand('git commit -am "dailyprogrammer-dl: Add title"',cwd=projectPath)

    return


def prependText( s, fn ):
    with open(fn,'r') as f:
        t = f.read()
    with open(fn,'w') as f:
        f.write(s)
        f.write(t)


def shellCommand( s, cwd=None ):
    logging.info("Executing shell command: {}".format(s))
    cl = shlex.split(s)
    proc=subprocess.Popen(cl,cwd=cwd)
    proc.wait()
    if( proc.returncode != 0 ):
        logging.error("Command failed: {}".format(s))


def moveFiles( files, dest ):
    for f in files:
        logging.info("Moving file {} to {}".format(f,dest))
        shutil.move(f,dest)


def downloadFile( src, dest ):
    logging.info("Saving {} to {}".format(src,dest))
    try:
        urllib.request.urlretrieve(src,dest)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            logging.error("Error downloading {}\nHTTP 404: Not Found {}".format(dest,src))
            pass
        else:
            raise


def generateProjectName( s ):
    m = re.search("Challenge #(\d+) \[(\w+)\] (.+)",s)
    if m:
        name = "{}{}-{}".format(m.group(1),m.group(2)[0].upper(),m.group(3).lower())
        name = re.sub(" ","-",name)
    else:
        name = s

    return name


if __name__ == "__main__":
    main()



