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
from .base import PyKeyboardMeta, PyKeyboardEventMeta

class PyKeyboard(PyKeyboardMeta):
    def press_key(self, key):
        event = CGEventCreateKeyboardEvent(None, key, True)
        CGEventPost(kCGHIDEventTap, event)

    def release_key(self, key):
        event = CGEventCreateKeyboardEvent(None, key, False)
        CGEventPost(kCGHIDEventTap, event)

class PyKeyboardEvent(PyKeyboardEventMeta):
    def run(self):
        tap = CGEventTapCreate(
            kCGSessionEventTap,
            kCGHeadInsertEventTap,
            kCGEventTapOptionDefault,
            CGEventMaskBit(kCGEventKeyDown) |
            CGEventMaskBit(kCGEventKeyUp),
            self.handler,
            None)

        loopsource = CFMachPortCreateRunLoopSource(None, tap, 0)
        loop = CFRunLoopGetCurrent()
        CFRunLoopAddSource(loop, loopsource, kCFRunLoopDefaultMode)
        CGEventTapEnable(tap, True)

        while self.state:
            CFRunLoopRunInMode(kCFRunLoopDefaultMode, 5, False)

    def handler(self, proxy, type, event, refcon):
        key = CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode)
        if type == kCGEventKeyDown:
            self.key_press(key)
        elif type == kCGEventKeyUp:
            self.key_release(key)
        
        if self.capture:
            CGEventSetType(event, kCGEventNull)

        return event
