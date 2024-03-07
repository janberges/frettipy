#!/usr/bin/env python3

"""Usage: frettipy [-f] FILE

This script formats Python source code following the below style conventions.

If `-f` is present, `FILE` **is modified in place!** Keep a copy or use version
control. Otherwise the intended modifications are shown without changing `FILE`.

If `FILE` is a directory, **all .py files in the directory tree are processed!**
"""

__version__ = '0.3'

import os
import re
import sys

def main():
    # parse arguments:

    modify = False

    for arg in sys.argv[1:]:
        if arg == '-f':
            modify = True
        else:
            filename = arg
            break
    else:
        print(__doc__)

        with open(__file__) as self:
            for rule in re.findall(r'# ([^a-z]+):', self.read()):
                print('*', rule.capitalize())

        return

    # process all Python files in directory tree:

    if os.path.isdir(filename):
        for path, folders, documents in os.walk(filename):
            folders[:] = [folder for folder in folders
                if not folder.startswith('.')]

            for document in documents:
                if document.startswith('.'):
                    continue

                if document.endswith('.py'):
                    script = os.path.join(path, document)

                    print('\033[0;32mPrettifying file %s\033[0m' % script)

                    prettifile(script, modify)
    else:
        prettifile(filename, modify)

def prettify(code):
    # functions to isolate groups and put them back:

    groups = []

    def replace(match):
        groups.append(match.group(0))
        return '___%d___' % len(groups)

    def place(match):
        return groups[int(match.group(0).strip('_')) - 1]

    def dereference(text):
        while True:
            text, count = re.subn(r'___\d+___', place, text)
            if not count:
                return text

    # isolate repeated quotes used as visual separators:

    code = re.sub(r'(\'\'){5,}|(""){5,}', replace, code, flags=re.DOTALL)

    # isolate strings:

    code = re.sub(r'(\'\'\'|""")(|[\w\W]*?[^\\])\1|(\'|")(|.*?[^\\])\3',
        replace, code)

    # isolate comments:

    code, N = re.subn('#.*', replace, code)

    for n in range(len(groups) - N, len(groups)):
        groups[n] = dereference(groups[n])

    # isolate expressions in brackets:

    while re.search('[([{]', code):
        count = 0

        for opener, closer in '()', '[]', '{}':
            code, N = re.subn(r'\%s[^()[\]{}]*\%s' % (opener, closer), replace,
                code)

            count += N

        if not count:
            print('\033[0;33mUnmatched parenthesis found!\033[0m')
            break

    # isolate NumPy arrays:

    code, N = re.subn(r'np\.array___\d+___', replace, code)

    for n in range(len(groups) - N, len(groups)):
        groups[n] = dereference(groups[n])

    # define overarching group for convenience:

    code = re.sub('.+', replace, code, flags=re.DOTALL)

    # define operators:

    unary = r'\+|-|~|\^'
    binary = r'\+|-|\*\*?|//?|%|&|\||<<|>>'
    comparison = '<=?|>=?|=='
    assignment = '(%s)?=' % binary

    # define keywords, some of which indicate start of expression:

    keywords = {'and', 'as', 'assert', 'async', 'await', 'break', 'class',
        'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for',
        'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal',
        'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'}

    # fix style of all groups:

    for n in range(len(groups)):
        if re.match(r'[\'"#]|np\.array', groups[n]):
            # PREFER SINGLE OVER DOUBLE QUOTATION MARK:
            groups[n] = re.sub(r'^"([^"\']*)"$', r"'\1'", groups[n])
            continue

        # isolate exponential numbers:
        groups[n] = re.sub('[0-9.]+e[+-]?[0-9]+', replace, groups[n])

        # DO NOT OMIT ZERO BEFORE OR AFTER DECIMAL POINT:
        groups[n] = re.sub(r'\b\d+\.\B', r'\g<0>0', groups[n])
        groups[n] = re.sub(r'\B\.\d+\b', r'0\g<0>', groups[n])

        # SPACES AROUND BINARY OPERATOR:
        groups[n] = re.sub(r'(\w+) *(%s) *(?=\w)' % binary,
            lambda match: ('%s %s' if match.group(1) in keywords else '%s %s ')
            % match.groups(), groups[n])

        # NO SPACE AFTER UNARY OPERATOR:
        groups[n] = re.sub(r'(?<![\w\s])( *(%s)) +(?=\w)' % unary, r'\1',
            groups[n])

        # isolate unary operators:
        groups[n] = re.sub(r'(%s)(?=\w)' % unary, replace, groups[n])

        # SPACES AROUND COMPARISON OPERATOR:
        groups[n] = re.sub(r'(?<=\w) *(%s) *(?=\w)' % comparison, r' \1 ',
            groups[n])

        if re.match('[([{]', groups[n]):
            # NO SPACES AROUND ARGUMENT-ASSIGNMENT OPERATOR:
            groups[n] = re.sub(r'(?<=\w) *= *(?=\w)', '=', groups[n])

            # NO SPACE ON INNER SIDE OF BRACKET:
            groups[n] = re.sub(r'([([{]) +(\S)', r'\1\2', groups[n])
            groups[n] = re.sub(r'(\S) +([)\]}])', r'\1\2', groups[n])

            if re.match(r'\[', groups[n]):
                # SLICES: NO SPACES AROUND SLICE OPERATOR:
                groups[n] = re.sub(r' *(:|\.{3}) *', r'\1', groups[n])

                # isolate slice operators:
                groups[n] = re.sub(r'(:|\.{3})', replace, groups[n])

            elif re.match(r'\{', groups[n]):
                # DICTIONARIES: SPACE AFTER COLON (BUT NOT BEFORE):
                groups[n] = re.sub(r'(?<=\w) *: *(?=\w)', ': ', groups[n])

        else:
            # SPACES AROUND ASSIGNMENT OPERATOR:
            groups[n] = re.sub(r'(?<=\w) *(%s) *(?=\w)' % assignment, r' \1 ',
                groups[n])

            # BLOCK INITIATION: NO SPACE BEFORE COLON:
            groups[n] = re.sub(r'(?<=\w) *:', ':', groups[n])

        # SPACE AFTER COMMA (BUT NOT BEFORE):
        groups[n] = re.sub(r'(?<=\w) *, *(?=\w)', ', ', groups[n])

        # NO DOUBLE SPACES:
        groups[n] = re.sub(r'(?<=\S) {2,}(?=\S)', ' ', groups[n])

        # SINGLE SPACE BETWEEN NON-WHITESPACE CHARACTER AND COMMENT:
        groups[n] = re.sub(r'(?<=\S)___\d+___', lambda match:
            (' ' if re.match('#', place(match)) else '') + match.group(0),
            groups[n])

        # NO SPACE BEFORE OPENING BRACKET (EXCEPT AFTER KEYWORD):
        groups[n] = re.sub(r'(\w+) *(___\d+___)', lambda match:
            match.group(1) + ' ' * (match.group(1) in keywords) + match.group(2)
            if re.match('[([{]', dereference(match.group(2))) else
            match.group(0), groups[n])

    # reinsert isolated groups:

    code = dereference(code)

    # INDENTATION WITH FOUR SPACES INSTEAD OF TABS:
    code = re.sub(r'\t', ' ' * 4, code)

    # NO TRAILING WHITESPACE:
    code = re.sub(' +$', '', code, flags=re.MULTILINE)

    # NO DOUBLE BLANK LINES:
    code = re.sub(r'\n{3,}', '\n' * 2, code)

    # NO BLANK LINE AT END OF FILE:
    code = re.sub(r'\n{2,}\Z', '\n' * 1, code)

    # NO BLANK LINE AT BEGINNING OF FILE:
    code = re.sub(r'\A\n{1,}', '\n' * 0, code)

    return code

def prettifile(filename, modify=True):
    # read file:

    with open(filename) as codefile:
        orig = codefile.read()

    # prettify code:

    code = prettify(orig)

    # write file:

    if code != orig:
        if modify:
            with open(filename, 'w') as codefile:
                codefile.write(code)
        else:
            import difflib

            for line in difflib.unified_diff(
                    orig.splitlines(), code.splitlines(),
                    fromfile=filename, tofile=filename, lineterm=''):

                print(line)

    # show (too) long lines:

    with open(filename) as codefile:
        for n, line in enumerate(codefile, 1):
            line = line.rstrip()

            if len(line) > 80:
                print('\033[0;33mLine %s exceeds 80 columns:\033[0m' % n)
                print(line)

if __name__ == '__main__':
    main()
