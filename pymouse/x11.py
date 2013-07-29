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

from Xlib.display import Display
from Xlib import X
from Xlib.ext.xtest import fake_input
from Xlib.ext import record
from Xlib.protocol import rq

from .base import PyMouseMeta, PyMouseEventMeta


class PyMouse(PyMouseMeta):
    def __init__(self, display=None):
        PyMouseMeta.__init__(self)
        self.display = Display(display)
        self.display2 = Display(display)

    def press(self, x, y, button=1):
        self.move(x, y)
        fake_input(self.display, X.ButtonPress, [None, 1, 3, 2, 4, 5][button])
        self.display.sync()

    def release(self, x, y, button=1):
        self.move(x, y)
        fake_input(self.display, X.ButtonRelease, [None, 1, 3, 2, 4, 5][button])
        self.display.sync()

    def scroll(self, vertical=None, horizontal=None, ticks=None):
        #Xlib does not support horizontal scrolling
        #Xlib does not support dynamic scrolling delta, only discrete ticks

        if horizontal is not None:
            print('Horizontal scrolling is not available on the X11 platform!')

        #For Xlib, ticks=True is implicit...
        if ticks is None or ticks is True:
            #Coerce vertical to an integer.
            vertical = int(vertical)
            if vertical == 0:  # No scrolling
                print('The scrolling value was 0!')
                return
            elif vertical > 0:  #Scroll up
                self.click(*self.position(), button=4, n=vertical)
            else:  #Scroll down
                self.click(*self.position(), button=5, n=abs(vertical))
        else:  #If ticks was passed as something else, warn and skip
            print('Warning: Received ticks={0}, resulting in no scrolling action!'.format(ticks))

    def oldscroll(self, x, y, up=False, n=1):
        #Xlib does not support horizontal scrolling
        if up is True:
            self.click(x, y, button=4, n=n)
        elif up is False:
            self.click(x, y, button=5, n=n)

    def move(self, x, y):
        if (x, y) != self.position():
            fake_input(self.display, X.MotionNotify, x=x, y=y)
            self.display.sync()

    def position(self):
        coord = self.display.screen().root.query_pointer()._data
        return coord["root_x"], coord["root_y"]

    def screen_size(self):
        width = self.display.screen().width_in_pixels
        height = self.display.screen().height_in_pixels
        return width, height

class PyMouseEvent(PyMouseEventMeta):
    def __init__(self, capture=False, capture_move=False, display=None):
        PyMouseEventMeta.__init__(self, capture=capture, capture_move=capture_move)
        self.display = Display(display)
        self.display2 = Display(display)
        self.ctx = self.display2.record_create_context(
            0,
            [record.AllClients],
            [{
                    'core_requests': (0, 0),
                    'core_replies': (0, 0),
                    'ext_requests': (0, 0, 0, 0),
                    'ext_replies': (0, 0, 0, 0),
                    'delivered_events': (0, 0),
                    'device_events': (X.ButtonPressMask, X.ButtonReleaseMask),
                    'errors': (0, 0),
                    'client_started': False,
                    'client_died': False,
            }])

    def run(self):
        try:
            if self.capture and self.capture_move:
                capturing = X.ButtonPressMask | X.ButtonReleaseMask | X.PointerMotionMask
            elif self.capture:
                capturing = X.ButtonPressMask | X.ButtonReleaseMask
            elif self.capture_move:
                capturing = X.PointerMotionMask
            else:
                capturing = False

            if capturing:
                self.display2.screen().root.grab_pointer(True,
                                                         capturing,
                                                         X.GrabModeAsync,
                                                         X.GrabModeAsync,
                                                         0, 0, X.CurrentTime)
                self.display.screen().root.grab_pointer(True,
                                                         capturing,
                                                         X.GrabModeAsync,
                                                         X.GrabModeAsync,
                                                         0, 0, X.CurrentTime)
    
            self.display2.record_enable_context(self.ctx, self.handler)
            self.display2.record_free_context(self.ctx)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.display.flush()
        self.display.record_disable_context(self.ctx)
        self.display.ungrab_pointer(X.CurrentTime)
        self.display2.flush()
        self.display2.record_disable_context(self.ctx)
        self.display2.ungrab_pointer(X.CurrentTime)

    def handler(self, reply):
        data = reply.data
        while len(data):
            event, data = rq.EventField(None).parse_binary_value(data, self.display.display, None, None)

            #In X11, the button numbers are: leftclick=1, middleclick=2,
            #  rightclick=3, scrollup=4, scrolldown=5
            #  For the purposes of the cross-platform interface of PyMouse, we
            #  invert the button number values of the right and middle buttons
            if event.type == X.ButtonPress:
                self.click(event.root_x, event.root_y, (None, 1, 3, 2, 4, 5, 3)[event.detail], True)
            elif event.type == X.ButtonRelease:
                self.click(event.root_x, event.root_y, (None, 1, 3, 2, 4, 5, 3)[event.detail], False)
            else:
                self.move(event.root_x, event.root_y)


