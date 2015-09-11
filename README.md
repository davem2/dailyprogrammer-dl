# dailyprogrammer-dl

Automates the initial setup of a www.reddit.com/r/dailyprogrammer/ project.

## Dependencies
  * docopt
  * html2text
  * robobrowser

## Usage

    python dailyprogrammer-dl.py http://www.reddit.com/r/dailyprogrammer/comments/3ggli3/20150810_challenge_227_easy_square_spirals/

Generates the project:

    227E-square-spirals/            # Auto generated project name
        227E-square-spirals.py      # Project file initialized with contents of boilerplate.txt
        README.md                   # Project description parsed from challenge page and converted to markdown

