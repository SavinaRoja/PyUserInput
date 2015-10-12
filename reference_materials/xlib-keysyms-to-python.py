#!/usr/bin/env python
# coding: utf-8
# Copyright 2015 Moses Palmér
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
"""
Converts the file xlib-keysyms.txt to a Python mapping from character to
symbol name.
"""

import os

#: The path to the input file
INPUT_PATH = os.path.join(
    os.path.dirname(__file__),
    'xlib-keysyms.txt')

#: The path to the output file
OUTPUT_PATH = os.path.join(
    os.path.dirname(__file__),
    os.path.pardir,
    'pykeyboard',
    'x11_keysyms.py')


def lines():
    """Yields all lines in the input file.
    """
    with open(INPUT_PATH) as f:
        for line in f:
            yield line.rstrip()


def keysym_lines():
    """Yields all lines in the input file containing a keysym definition.
    """
    for line in lines():
        if not line:
            # Ignore empty lines
            continue
        elif line[0] == '#':
            # Ignore lines starting with '#'; it is also used to separate
            # keysym information from its name, but in the first position it is
            # used to mark comments
            continue
        else:
            yield line


def keysym_definitions():
    """Yields all keysym definitions parsed as tuples.
    """
    for keysym_line in keysym_lines():
        # As described in the input text, the format of a line is:
        # 0x20 U0020 . # space /* optional comment */
        keysym_number, codepoint, status, _, name_part = [
            p.strip() for p in keysym_line.split(None, 4)]
        name = name_part.split()[0]

        yield (int(keysym_number, 16), codepoint[1:], status, name)


def keysyms_from_strings():
    """Yields the tuple ``(character, symbol name)`` for all keysyms.
    """
    for number, codepoint, status, name in keysym_definitions():
        # Ignore keysyms that do not map to unicode characters
        if all(c == '0' for c in codepoint):
            continue

        # Ignore keysyms that are not well established
        if status != '.':
            continue

        yield (codepoint, name)


if __name__ == '__main__':
    with open(OUTPUT_PATH, 'w') as f:
        f.write('''# coding: utf-8
# Copyright 2015 Moses Palmér
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

KEYSYMS = {
%s}
''' % ',\n'.join(
            '    u\'\\u%s\': \'%s\'' % (codepoint, name)
            for codepoint, name in keysyms_from_strings()))
