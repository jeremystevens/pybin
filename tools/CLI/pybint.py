#!/usr/bin/python
import argparse
import requests

# headers do not change this!
__author__ = 'Jeremy Stevens'
__license__ = 'GPL'
__version__ = '1.0.0'
__maintainer__ = 'Jeremy Stevens'
__email__ = 'Jeremiahstevens@gmail.com'
__status__ = 'Production'

""""
EDIT SERVER ADDRESS BELOW FOR YOUR SERVER 
make sure the to leave the /api at the end of the URL.
ex. (http://www.yourserver.com/api)
"""

# SERVER ADDRESS
SERVER = f"http://127.0.0.1:5000/api"

# Args list
parser = argparse.ArgumentParser(description='pybint', usage='%(prog)s [-insex]')
parser.add_argument('-i', '--input', help='Input file name', required=True)
parser.add_argument('-n', '--name', help='paste name', required=False)
parser.add_argument('-s', '--syntax', help='paste name', required=False)
parser.add_argument('-e', '--expire', help='paste expire', required=False)
# 0 = never, 1= 10 min, 2 = 1 hour, 3 = 1 day, 4 = 1 month
parser.add_argument('-x', '--exposure', help='paste exposure', required=False)
args = parser.parse_args()

# open the file
fo = open(args.input, "r+")
# read the file and put it in a var
str = fo.read();

# check if vars are set and strip whitespace and  if not set use default values.
if args.name:
    name = args.name.strip()
if not args.name:
    # if no title name it "Untitled"
    name = "untitled"
str = str.strip()
if args.syntax:
    syntax = args.syntax.strip()
if not args.syntax:
    # if not set then set  the default to plain text
    syntax = "text"
if args.expire:
    expire = args.expire.strip()
if not args.expire:
    # if not set then set the default to 10 mins
    expire = "1"
if args.exposure:
    exposure = args.exposure.strip()
if not args.exposure:
    # if not set then set the default to "public"
    exposure = "Public"

# payload
payload = {'paste_title': name, 'paste_syntax': syntax, 'paste_exp': expire, 'exposure': exposure, 'paste_text': str}
# webrequest
r = requests.post(SERVER, data=payload)
status = r.status_code
text = r.text
if status == 200:
    split_string = SERVER.split("/api", 1)
    substring = split_string[0]
    url = substring + "/p/" + text
    print("Post URL: " + url)
else:
    print("Error Please try again")
