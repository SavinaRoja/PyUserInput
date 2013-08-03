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

    def __init__(self):
        self.vertical_tick_delta = 1.0
        self.horizontal_tick_delta = 1.0

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

    def scroll(self, vertical=None, horizontal=None, depth=None,
               dynamic=None):
        """
        This function seeks to provide a uniform interface across platforms for
        scrolling. This is made somewhat tricky due to different scrolling
        support between platforms. Ideally each platform''s full flexiblity will
        be preserved, while maintaining an easy means to code cross-platform
        scrolling actions.

        All platforms support scrolling in at least two axes: "horizontal" and
        "vertical". Mac supports a third axis named "depth", which cannot be
        emulated on the other platforms. Values for these arguments may be
        positive or negative numbers (float or int). Refer to the following
        mapping of sign to direction:
            Vertical: + Up, - Down
            Horizontal: + Right, - Left
            Depth: + Rise (out of display), - Dive (towards display)

        The default scrolling behavior is to treat the arguments as a integer
        quantity of "ticks"; this is the way to provide cross-platform
        scrolling. In this mode, the scrolling will be generated as a series of
        discretized scroll events.

        The other method is to pass True to the "dynamic" argument; this is
        only cross-platform for Mac and Windows (Xlib does not support dynamic
        distance in scrolling events). In this mode, one can utilize the
        dynamic scroll distance support provided by the platform to scroll a
        specified number of pixels. A single scroll event will be generated
        with the pixel distances provided.
        """

        raise NotImplementedError

    def set_scroll_delta(self, vertical=None, horizontal=None):
        """Sets the scroll delta for scrolling by tick"""

        def check_val(value):
            """Return False if rejected, True if acceptable"""
            try:
                if vertical <0:  # Less than 0 is rejected
                    print('Error: Tick-Delta values should be greater than 0')
                    return False
                elif vertical > 10:  # Warn about values greater than 10, but accept
                    print('Warning: Tick-Delta values greater than 10 are not recommended')
                    return True
                else:  # Accept any number between 0 and 10
                    return True
            except TypeError:  # Passed a non-number value
                print('Error: Tick-Delta values should be integers or floats')
                return False

        if vertical is not None:
            if check_val(vertical):
                self.vertical_tick_delta = float(vertical)
        if horizontal is not None:
            if check_val(horizontal):
                self.horizontal_tick_delta = float(horizontal)

    def move(self, x, y):
        """Move the mouse to a given x and y"""

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
