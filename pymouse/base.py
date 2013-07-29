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
The goal of PyMouse is to have a cross-platform way to control the mouse.
PyMouse should work on Windows, Mac and any Unix that has xlib.

As the base file, this provides a rough operational model along with the
framework to be extended by each platform.
"""

from threading import Thread

class PyMouseMeta(object):

    def press(self, x, y, button=1):
        """
        Press the mouse on a given x, y and button.
        Button is defined as 1 = left, 2 = right, 3 = middle.
        """

        raise NotImplementedError

    def release(self, x, y, button=1):
        """
        Release the mouse on a given x, y and button.
        Button is defined as 1 = left, 2 = right, 3 = middle.
        """

        raise NotImplementedError

    def click(self, x, y, button=1, n=1):
        """
        Click a mouse button n times on a given x, y.
        Button is defined as 1 = left, 2 = right, 3 = middle.
        """

        for i in range(n):
            self.press(x, y, button)
            self.release(x, y, button)

    def scroll(self, x, y, up=False, n=1):
        """
        Scroll using the mouse wheel at a given x, y.

        Pass up=True to scroll upwards and pass up=False to scroll downwards.
        Pass a nonzero integer to the n argument to scroll that many "ticks".
        """

        raise NotImplementedError

    def move(self, x, y):
        """Move the mouse to a given x and y"""

        raise NotImplementedError

    def drag(self, x, y):
        """Drag the mouse to a given x and y.
        A Drag is a Move where the mouse key is held down."""

        raise NotImplementedError

    def position(self):
        """
        Get the current mouse position in pixels.
        Returns a tuple of 2 integers
        """

        raise NotImplementedError

    def screen_size(self):
        """
        Get the current screen size in pixels.
        Returns a tuple of 2 integers
        """

        raise NotImplementedError

class PyMouseEventMeta(Thread):
    def __init__(self, capture=False, capture_move=False):
        Thread.__init__(self)
        self.daemon = True
        self.capture = capture
        self.capture_move = capture_move
        self.state = True

    def stop(self):
        self.state = False

    def click(self, x, y, button, press):
        """Subclass this method with your click event handler"""
        pass

    def move(self, x, y):
        """Subclass this method with your move event handler"""
        pass
