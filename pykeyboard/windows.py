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

import win32api, win32con

import time

class PyKeyboard(PyKeyboardMeta):
    """
    The PyKeyboard implementation for Windows systems. This allows one to
    simulate keyboard input.
    """
    def __init__(self):
        PyKeyboardMeta.__init__(self)

    def press_key(self, character=''):
        win32api.keybd_event(win32com.WM_KEYDOWN)

    def release_key(self, character=''):
        win32api.keybd_event(win32com.WM_KEYUP)

    def tap_key(self, character='', repeat=1):
        """
        Press and release a given character key n times.
        """
        for i in xrange(repeat):
            self.press_key(character)
            self.release_key(character)