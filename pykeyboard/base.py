"""
Provides the operational model. 
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

    def tap_key(self, character='', n=1):
        """Press and release a given character key n times."""
        for i in xrange(n):
            self.press_key(character)
            self.release_key(character)
        raise NotImplementedError

    def type_string(self, char_string, char_interval=0):
        """A convenience method for typing longer strings of characters."""
        for i in char_string:
            time.sleep(char_interval)
            self.tap_key(i)
        raise NotImplementedError

    def special_key_assignment(self):
        """Makes special keys more accessible."""
        raise NotImplementedError

    def lookup_character_value(self, character):
        """
        If necessary, lookup a valid API value for the key press from the
        character.
        """
        raise NotImplementedError

class PyKeyboardEventMeta(Thread):
    """
    The base class for PyKeyboard. Represents basic operational model.
    """
    def __init__(self, capture=False, captureMove=False):
        Thread.__init__(self)
        self.daemon = True
        self.capture = capture
        self.captureMove = captureMove
        self.state = True

    def run(self):
        self.state = True

    def stop(self):
        self.state = False

    def handler(self):
        pass

    def key_press(self, key):
        """Subclass this method with your key press event handler."""
        pass

    def key_release(self, key):
        """Subclass this method with your key release event handler."""
        pass

    def escape_code(self):
        """
        Defines a means to signal a stop to listening. Subclass this with your
        escape behavior.
        """
        escape = None
        return escape
