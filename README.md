# frettipy

No fretting about pretty Python.

* Prefer single over double quotation mark
* Do not omit zero before or after decimal point
* Spaces around binary operator
* No space after unary operator
* Spaces around comparison operator
* No spaces around argument-assignment operator
* No space on inner side of bracket
* No explicit line joining in brackets
* Slices: no spaces around slice operator
* Dictionaries: space after colon (but not before)
* Same indentation of lines with opening and closing bracket
* Spaces around assignment operator
* Block initiation: no space before colon
* Space after comma (but not before)
* No double spaces
* Single space between non-whitespace character and comment
* No space before opening bracket (except after keyword)
* Indentation with four spaces instead of tabs
* No trailing whitespace
* No double blank lines (except before class or function)
* No blank line at end of file
* No blank line at beginning of file
* Newline character at end of last line

## Synopsis

This script formats Python source code following the above style conventions.

    frettipy [-f] FILE

If `-f` is present, `FILE` **is modified in place!** Keep a copy or use version
control. Otherwise the intended modifications are shown without changing `FILE`.

If `FILE` is a directory, **all .py and .Rmd files in the tree are processed!**

## Installation

Either from PyPI:

    python3 -m pip install frettipy

Or from GitHub:

    python3 -m pip install git+https://github.com/janberges/frettipy
