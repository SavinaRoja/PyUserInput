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

from ctypes import *
import win32api, win32con
from .base import PyMouseMeta, PyMouseEventMeta
import pythoncom, pyHook
from time import sleep

class POINT(Structure):
    _fields_ = [("x", c_ulong),
                ("y", c_ulong)]

class PyMouse(PyMouseMeta):
    """MOUSEEVENTF_(button and action) constants 
    are defined at win32con, buttonAction is that value"""
    def press(self, x, y, button = 1):
        buttonAction = 2**((2*button)-1)
        self.move(x,y)
        win32api.mouse_event(buttonAction, x, y)
     
    def release(self, x, y, button = 1):
        buttonAction = 2**((2*button))
        self.move(x,y)
        win32api.mouse_event(buttonAction, x, y)

    def move(self, x, y):
        windll.user32.SetCursorPos(x, y)

    def position(self):
        pt = POINT()
        windll.user32.GetCursorPos(byref(pt))
        return pt.x, pt.y

    def screen_size(self):
        width = windll.user32.GetSystemMetrics(0)
        height = windll.user32.GetSystemMetrics(1)
        return width, height

class PyMouseEvent(PyMouseEventMeta):
    def __init__(self):
        PyMouseEventMeta.__init__(self)
        self.hm = pyHook.HookManager()

    def run(self):
        self.hm.MouseAllButtons = self._click
        self.hm.MouseMove = self._move
        #I think I can add scrollwheel support at some point
        self.hm.HookMouse()
        while self.state:
            sleep(0.01)
            pythoncom.PumpWaitingMessages()

    def stop(self):
        self.hm.UnhookMouse()
        self.state = False

    def _click(self, event):
        x,y = event.Position

        if event.Message == pyHook.HookConstants.WM_LBUTTONDOWN:
            self.click(x, y, 1, True)
        elif event.Message == pyHook.HookConstants.WM_LBUTTONUP:
            self.click(x, y, 1, False)
        elif event.Message == pyHook.HookConstants.WM_RBUTTONDOWN:
            self.click(x, y, 2, True)
        elif event.Message == pyHook.HookConstants.WM_RBUTTONUP:
            self.click(x, y, 2, False)
        elif event.Message == pyHook.HookConstants.WM_MBUTTONDOWN:
            self.click(x, y, 3, True)
        elif event.Message == pyHook.HookConstants.WM_MBUTTONUP:
            self.click(x, y, 3, False)
        return not self.capture

    def _move(self, event):
        x,y = event.Position
        self.move(x, y)
        return not self.captureMove
