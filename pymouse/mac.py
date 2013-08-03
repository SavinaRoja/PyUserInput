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

from Quartz import *
from AppKit import NSEvent
from .base import PyMouseMeta, PyMouseEventMeta

pressID = [None, kCGEventLeftMouseDown,
           kCGEventRightMouseDown, kCGEventOtherMouseDown]
releaseID = [None, kCGEventLeftMouseUp,
             kCGEventRightMouseUp, kCGEventOtherMouseUp]


class PyMouse(PyMouseMeta):

    def press(self, x, y, button=1):
        event = CGEventCreateMouseEvent(None,
                                        pressID[button],
                                        (x, y),
                                        button - 1)
        CGEventPost(kCGHIDEventTap, event)

    def release(self, x, y, button=1):
        event = CGEventCreateMouseEvent(None,
                                        releaseID[button],
                                        (x, y),
                                        button - 1)
        CGEventPost(kCGHIDEventTap, event)

    def move(self, x, y):
        move = CGEventCreateMouseEvent(None, kCGEventMouseMoved, (x, y), 0)
        CGEventPost(kCGHIDEventTap, move)

    def position(self):
        loc = NSEvent.mouseLocation()
        return loc.x, CGDisplayPixelsHigh(0) - loc.y

    def screen_size(self):
        return CGDisplayPixelsWide(0), CGDisplayPixelsHigh(0)

    def scroll(self, vertical=None, horizontal=None, ticks=None,
               tick_delta_v=None, tick_delta_h=None):
        #Mac has the greatest scrolling functionality: supporting 3 dimensions
        #of scrolling and dynamic scroll distance events (in pixels or lines)

        def scroll_event(y_movement, x_movement):
            #Movements should be no larger than +- 10
            scrollWheelEvent = CGEventCreateScrollWheelEvent(
                None,  # No source
                kCGScrollEventUnitPixel,  # We are using pixel units
                2,  # Number of wheels(dimensions)
                y_movement,
                x_movement)
            CGEventPost(kCGHIDEventTap, scrollWheelEvent)

        if ticks is True:  # Ticks will override, and expect integers
            #Get the tick_deltas
            if tick_delta_v is None:
                tick_delta_v = self.vertical_tick_delta
            if tick_delta_h is None:
                tick_delta_h = self.horizontal_tick_delta
            #Execute vertical scroll ticks
            if vertical is not None:
                vertical = int(vertical)
                if vertical == 0:  # No scrolling
                    print('The vertical scrolling value was 0!')
                elif vertical > 0:  # Scroll up
                    for i in range(vertical):
                        scroll_event(tick_delta_v, 0)
                else:  # Scroll down
                    for i in range(abs(vertical)):
                        scroll_event(-1 * tick_delta_v, 0)
            #Execute horizontal scroll ticks
            if horizontal is not None:
                horizontal = int(horizontal)
                if horizontal == 0:  # No scrolling
                    print('The horizontal scrolling value was 0!')
                elif horizontal > 0:  # Scroll up
                    for i in range(horizontal):
                        scroll_event(0, tick_delta_h)
                else:  # Scroll down
                    for i in range(abs(horizontal)):
                        scroll_event(0, -1 * tick_delta_h)

        elif ticks is None:  # If not ticks, expect either floats or integers
            if vertical is not None and horizontal is not None:
                scroll_event(vertical, horizontal)
            elif vertical is not None:
                scroll_event(vertical, 0)
            elif horizontal is not None:
                scroll_event(0, horizontal)


class PyMouseEvent(PyMouseEventMeta):
    def run(self):
        tap = CGEventTapCreate(
            kCGSessionEventTap,
            kCGHeadInsertEventTap,
            kCGEventTapOptionDefault,
            CGEventMaskBit(kCGEventMouseMoved) |
            CGEventMaskBit(kCGEventLeftMouseDown) |
            CGEventMaskBit(kCGEventLeftMouseUp) |
            CGEventMaskBit(kCGEventRightMouseDown) |
            CGEventMaskBit(kCGEventRightMouseUp) |
            CGEventMaskBit(kCGEventOtherMouseDown) |
            CGEventMaskBit(kCGEventOtherMouseUp),
            self.handler,
            None)

        loopsource = CFMachPortCreateRunLoopSource(None, tap, 0)
        loop = CFRunLoopGetCurrent()
        CFRunLoopAddSource(loop, loopsource, kCFRunLoopDefaultMode)
        CGEventTapEnable(tap, True)

        while self.state:
            CFRunLoopRunInMode(kCFRunLoopDefaultMode, 5, False)

    def handler(self, proxy, type, event, refcon):
        (x, y) = CGEventGetLocation(event)
        if type in pressID:
            self.click(x, y, pressID.index(type), True)
        elif type in releaseID:
            self.click(x, y, releaseID.index(type), False)
        else:
            self.move(x, y)

        if self.capture:
            CGEventSetType(event, kCGEventNull)

        return event
