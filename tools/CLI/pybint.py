#!/usr/bin/python

"""
pybint.py -  A CLI tool to upload to pybin
"""

# Copyright 2022 Jeremy Stevens <jeremiahstevens@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
__version__ = '1.0.0'

# ============================================================

import argparse
import requests

""""
EDIT SERVER ADDRESS BELOW FOR YOUR SERVER 
make sure to leave the /api at the end of the URL.
ex. (http://www.yourserver.com/api)
"""

# SERVER ADDRESS
SERVER = f"http://127.0.0.1:5000/api"

""" 
==== EXPOSURE ======
  - public 
  - unlisted (not shown in archive can only access if you know the uid)
"""

""" 
==== Expire Numbers =====
  0 = Never Expires 
  1 = 10 minutes 
  2 = 1 Hour
  3 = 1 Day 
  4 = 1 Month 
"""

""" 
==== SUPPORTED SYNTAX LIST (292 syntax) ======
abap
abnf
actionscript
ada
agda
al
antlr4
apacheconf
apex
apl
applescript
aql
arduino
arff
arm-asm
arturo
asciidoc
aspnet
asm6502
asmatmel
autohotkey
autoit
avisynth
avrodl
awk
bash
basic
batch
bbcode
bicep
birb
bison
bnf
brainfuck
brightscript
bro
bsl
c
csharp
cpp
cfscript
chaiscript
cil
clojure
cmake
cobol
coffeescript
concurnas
csp
cooklang
coq
crystal
css-extras
csv
cue
cypher
d
dart
dataweave
dax
dhall
diff
django
dns-zone-file
docker
dot
ebnf
editorconfig
eiffel
ejs
elixir
elm
etlua
erb
erlang
excel-formula
fsharp
factor
false
firestore-security-rules
flow
fortran
ftl
gamemakerlanguage
gap
gcode
gdscript
gedcom
gettext
gherkin
git
glsl
gn
linker-script
go
go-module
gradle
graphql
groovy
haml
handlebars
haskell
haxe
hcl
hlsl
hoon
http
hpkp
hsts
ichigojam
icon
icu-message-format
idris
ignore
inform7
ini
io
j
java
javadoc
javadoclike
javastacktrace
Javascript 
jexl
jolie
jq
jsdoc
js-extras
json
json5
jsonp
jsstacktrace
js-templates
julia
keepalived
keyman
kotlin
kumir
kusto
latex
latte
less
lilypond
liquid
lisp
livescript
llvm
log
lolcode
lua
magma
makefile
markdown
markup-templating
mata
matlab
maxscript
mel
mermaid
mizar
mongodb
monkey
moonscript
n1ql
n4js
nand2tetris-hdl
naniscript
nasm
neon
nevod
nginx
nim
nix
nsis
objectivec
ocaml
odin
opencl
openqasm
oz
parigp
parser
pascal
pascaligo
psl
pcaxis
peoplecode
perl
php
phpdoc
php-extras
plant-uml
plsql
powerquery
powershell
processing
prolog
promql
properties
protobuf
pug
puppet
pure
purebasic
purescript
python
qsharp
q
qml
qore
r
racket
cshtml
jsx
tsx
reason
regex
rego
renpy
rescript
rest
rip
roboconf
robotframework
ruby
rust
sas
sass
scss
scala
scheme
shell-session
smali
smalltalk
smarty
sml
solidity
solution-file
soy
sparql
splunk-spl
sqf
sql
squirrel
stan
stata
iecst
stylus
supercollider
swift
systemd
t4-templating
t4-cs
t4-vb
tap
tcl
tt2
text
textile
toml
tremor
turtle
twig
typescript
typoscript
unrealscript
uorazor
uri
v
Vala - vala
VB.Net - vbnet
Velocity - velocity
verilog
vhdl
vim
visual-basic
warpscript
wasm
webdl
wgsl
wiki
wolfram
wren
xeora
xml-doc
xojo
xquery
yaml
yang
zig 
"""

'''' EXAMPLE USAGE'''
# python pybint.py -i inputfile.py -n helloworld -s python -e 1 -x public
""" END OF EXAMPLE USAGE """

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
str = fo.read()

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
