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
