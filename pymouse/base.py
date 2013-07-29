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

    def scroll(self, vertical=None, horizontal=None, ticks=None, tick_delta=1):
        """
        The scrolling function attempts to provide a uniform interface across
        the different platforms; it faces difficulty in that not all actions
        are possible on every platform. The differences will be itemized in
        each platform's sub-class. The following guidelines should be kept in
        mind: all actions supported by a platform should be available, actions
        which are not possible on the present platform (not cross-compatible)
        should raise an informative error.

        Vertical scrolling is available on all platforms, and may be controlled
        by the vertical argument. Values may be float or int, and should not
        have a magnitude greater than 10. Positive values will scroll up, and
        negative values will scroll down.
        
        Horizontal scrolling is available only on Mac, and is controlled by the
        horizontal argument. Acceptable values are as for vertical; positive
        will scroll right and negative will scroll left.

        Scrolling may also be controlled as a series of "ticks" by passing an
        integer to the ticks argument. This is critically important in the
        provision of scrolling for X11, which treats scrolling as a series of
        button presses. For Mac and Windows, the movement delta for scrolling
        by tick value can be modified using the tick_delta argument. The ticks
        argument

        

        """

        raise NotImplementedError

    def set_scroll_tick_delta(self, vertical=None, horizontal=None):
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
