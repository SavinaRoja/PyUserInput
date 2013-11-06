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
As the base file, this provides a rough operational model along with the
framework to be extended by each platform.
"""

import time
from threading import Thread

class PyKeyboardMeta(object):
    """
    The base class for PyKeyboard. Represents basic operational model.
    """

    def press_key(self, character=''):
        """Press a given character key."""
        raise NotImplementedError

    def release_key(self, character=''):
        """Release a given character key."""
        raise NotImplementedError

    def tap_key(self, character='', n=1, interval=0):
        """Press and release a given character key n times."""
        for i in range(n):
            self.press_key(character)
            self.release_key(character)
            time.sleep(interval)

    def type_string(self, char_string, interval=0):
        """A convenience method for typing longer strings of characters."""
        for i in char_string:
            time.sleep(interval)
            self.tap_key(i)

    def special_key_assignment(self):
        """Makes special keys more accessible."""
        raise NotImplementedError

    def lookup_character_value(self, character):
        """
        If necessary, lookup a valid API value for the key press from the
        character.
        """
        raise NotImplementedError

    def is_char_shifted(self, character):
        """Returns True if the key character is uppercase or shifted."""
        if character.isupper():
            return True
        if character in '<>?:"{}|~!@#$%^&*()_+':
            return True
        return False

class PyKeyboardEventMeta(Thread):
    """
    The base class for PyKeyboard. Represents basic operational model.
    """
    def __init__(self, capture=False):
        Thread.__init__(self)
        self.daemon = True
        self.capture = capture
        self.state = True

    def run(self):
        self.state = True

    def stop(self):
        self.state = False

    def handler(self):
        raise NotImplementedError

    def tap(self, keycode, character, press):
        """
        Subclass this method with your key event handler. It will receive
        the keycode associated with the key event, as well as string name for
        the key if one can be assigned (keyboard mask states will apply). The
        argument 'press' will be True if the key was depressed and False if the
        key was released.
        """
        pass

    def escape(self, event):
        """
        A function that defines when to stop listening; subclass this with your
        escape behavior. If the program is meant to stop, this method should
        return True. Every key event will go through this method before going to
        tap(), allowing this method to check for exit conditions.

        The default behavior is to stop when the 'Esc' key is pressed.

        If one wishes to use key combinations, or key series, one might be
        interested in reading about Finite State Machines.
        http://en.wikipedia.org/wiki/Deterministic_finite_automaton
        """
        condition = None
        return event == condition
