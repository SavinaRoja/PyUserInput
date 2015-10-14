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
    #: We add this named character for convenience
    space = ' '

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

    def press_keys(self,characters=[]):
        """Press a given character key."""
        for character in characters:
            self.press_key(character)
        for character in characters:
            self.release_key(character)

    def type_string(self, char_string, interval=0):
        """
        A convenience method for typing longer strings of characters. Generates
        as few Shift events as possible."""
        shift = False
        for char in char_string:
            if self.is_char_shifted(char):
                if not shift:  # Only press Shift as needed
                    time.sleep(interval)
                    self.press_key(self.shift_key)
                    shift = True
                #In order to avoid tap_key pressing Shift, we need to pass the
                #unshifted form of the character
                if char in '<>?:"{}|~!@#$%^&*()_+':
                    ch_index = '<>?:"{}|~!@#$%^&*()_+'.index(char)
                    unshifted_char = ",./;'[]\\`1234567890-="[ch_index]
                else:
                    unshifted_char = char.lower()
                time.sleep(interval)
                self.tap_key(unshifted_char)
            else:  # Unshifted already
                if shift and char != ' ':  # Only release Shift as needed
                    self.release_key(self.shift_key)
                    shift = False
                time.sleep(interval)
                self.tap_key(char)

        if shift:  # Turn off Shift if it's still ON
            self.release_key(self.shift_key)

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

    #One of the most variable components of keyboards throughout history and
    #across manufacturers is the Modifier Key...
    #I am attempting to cover a lot of bases to make using PyKeyboardEvent
    #simpler, without digging a bunch of traps for incompatibilities between
    #platforms.

    #Keeping track of the keyboard's state is not only necessary at times to
    #correctly interpret character identities in keyboard events, but should
    #also enable a user to easily query modifier states without worrying about
    #chaining event triggers for mod-combinations

    #The keyboard's state will be represented by an integer, the individual
    #mod keys by a bit mask of that integer
    state = 0

    #Each platform should assign, where applicable/possible, the bit masks for
    #modifier keys initially set to 0 here. Not all modifiers are recommended
    #for cross-platform use
    modifier_bits = {'Shift': 1,
                     'Lock': 2,
                     'Control': 4,
                     'Mod1': 8,  # X11 dynamic assignment
                     'Mod2': 16,  # X11 dynamic assignment
                     'Mod3': 32,  # X11 dynamic assignment
                     'Mod4': 64,  # X11 dynamic assignment
                     'Mod5': 128,  # X11 dynamic assignment
                     'Alt': 0,
                     'AltGr': 0,  # Uncommon
                     'Caps_Lock': 0,
                     'Command': 0,  # Mac key without generic equivalent
                     'Function': 0,  # Not advised; typically undetectable
                     'Hyper': 0,  # Uncommon?
                     'Meta': 0,  # Uncommon?
                     'Num_Lock': 0,
                     'Mode_switch': 0,  # Uncommon
                     'Shift_Lock': 0,  # Uncommon
                     'Super': 0,  # X11 key, sometimes equivalent to Windows
                     'Windows': 0}  # Windows key, sometimes equivalent to Super

    #Make the modifiers dictionary for individual states, setting all to off
    modifiers = {}
    for key in modifier_bits.keys():
        modifiers[key] = False

    def __init__(self, capture=False):
        Thread.__init__(self)
        self.daemon = True
        self.capture = capture
        self.state = True
        self.configure_keys()

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

    def configure_keys(self):
        """
        Does per-platform work of configuring the modifier keys as well as data
        structures for simplified key access. Does nothing in this base
        implementation.
        """
        pass
