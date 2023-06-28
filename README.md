# frettipy

No fretting about pretty Python.

* Prefer single over double quotation marks
* Do not omit zero before or after decimal point
* Spaces around binary operators
* No space after unary operators
* Spaces around comparison operators
* No spaces around the argument-assignment operator
* No spaces on the inner side of brackets
* Slices: no spaces around slice operators
* Dictionaries: spaces after colon (but not before)
* Spaces around assignment operators
* Block initiation: no spaces before colon
* Spaces after commas (but not before)
* No double spaces
* Single space between non-whitespace character and comment
* No space before opening bracket (except after keyword)
* Four spaces instead of tabs
* No trailing whitespace
* No double blank lines
* No blank line at end of file
* No blank line at beginning of file

## Synopsis

This script formats Python source code following the above style conventions.

    frettipy [-f] [-r] FILE

If `-f` is present, `FILE` **is modified in place!** Keep a copy or use version
control. Otherwise the intended modifications are shown without changing `FILE`.

If `-r` is present and `FILE` is a directory, **all .py files in the directory
tree are processed!**

## Installation

Either from PyPI:

    python3 -m pip install frettipy

Or from GitHub:

    python3 -m pip install git+https://github.com/janberges/frettipy
