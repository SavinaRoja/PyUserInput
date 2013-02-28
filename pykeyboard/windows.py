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
        """
        Press a given character key.
        """
        char_vk = win32api.VkKeyScan(character)
        win32api.keybd_event(char_vk, 0, 0, 0)

    def release_key(self, character=''):
        """
        Release a given character key.
        """
        char_vk = win32api.VkKeyScan(character)
        win32api.keybd_event(char_vk, 0, win32com.KEYEVENTF_KEYUP, 0)

    def tap_key(self, character='', repeat=1, char_interval=0):
        """
        Press and release a given character key repeat=n times.
        """
        for i in xrange(repeat):
            self.press_key(character)
            self.release_key(character)
            time.sleep(char_interval)

    def type_string(self, char_string, char_interval=0):
        """
        A convenience method for typing longer strings of characters.
        """
        for i in char_string:
            self.tap_key(i)
            time.sleep(char_interval)

    def is_char_shifted(self, character):
        """Returns True if the key character is uppercase or shifted."""
        if character.isupper():
            return True
        if character in '<>?:"{}|~!@#$%^&*()_+':
            return True
        return False