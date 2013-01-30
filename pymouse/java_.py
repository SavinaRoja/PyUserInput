# -*- coding: iso-8859-1 -*-

#   Copyright 2010 Pepijn de Vos
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from java.awt import Robot, Toolkit
from java.awt.event import InputEvent
from java.awt.MouseInfo import getPointerInfo
from base import PyMouseMeta

r = Robot()

class PyMouse(PyMouseMeta):
    def press(self, x, y, button = 1):
        button_list = [None, InputEvent.BUTTON1_MASK, InputEvent.BUTTON3_MASK, InputEvent.BUTTON2_MASK]
        self.move(x, y)
        r.mousePress(button_list[button])

    def release(self, x, y, button = 1):
        button_list = [None, InputEvent.BUTTON1_MASK, InputEvent.BUTTON3_MASK, InputEvent.BUTTON2_MASK]
        self.move(x, y)
        r.mouseRelease(button_list[button])
    
    def move(self, x, y):
        r.mouseMove(x, y)

    def position(self):
        loc = getPointerInfo().getLocation()
        return loc.getX, loc.getY

    def screen_size(self):
        dim = Toolkit.getDefaultToolkit().getScreenSize()
        return dim.getWidth(), dim.getHeight()
