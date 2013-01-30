#Copyright 2013 Paul Barton
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
The goal of PyKeyboard is to provide a cross-platform way to control the
keyboard. It is intended to be complementary to the PyMouse module by
pepijndevos and should work on the same dependencies.

PyKeyboard should work on Windows, Mac, and X11 systems.

For more information about PyKeyboard, see:
See http://github.com/SavinaRoja/PyKeyboard

And for PyMouse:
See http://github.com/pepijndevos/PyMouse
"""

import sys

if sys.platform.startswith('java'):
    from java_ import PyKeyboard

elif sys.platform == 'darwin':
    from mac import PyKeyboard, PyKeyboardEvent

elif sys.platform == 'win32':
    from windows import PyKeyboard, PyKeyboardEvent

else:
    from x11 import PyKeyboard, PyKeyboardEvent
