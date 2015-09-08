'''
Tested on linux.

install:  Xvfb, Xephyr, PyVirtualDisplay, nose

on Ubuntu:

    sudo apt-get install python-nose
    sudo apt-get install xvfb
    sudo apt-get install xserver-xephyr
    sudo apt-get install python-setuptools
    sudo easy_install PyVirtualDisplay

to start:

    nosetests -v
'''

from nose.tools import eq_
from pymouse import PyMouse, PyMouseEvent
from pyvirtualdisplay import Display
from unittest import TestCase
import time

# 0 -> Xvfb
# 1 -> Xephyr
VISIBLE = 0

screen_sizes = [
              (10, 20),
              (100, 200),
              (765, 666),
              ]
positions = [
              (0, 5),
              (0, 0),
              (10, 20),
              (-10, -20),
              (2222, 2222),
              (5, 0),
              (9, 19),
              ]

buttons = [1, 2, 3, 10]  # 10 = mouse btn6

class Event(PyMouseEvent):
    def reset(self):
        self.pos = None
        self.button = None
        self.press = None
        self.scroll_vertical = None
        self.scroll_horizontal = None

    def move(self, x, y):
        print("Mouse moved to", x, y)
        self.pos = (x, y)

    def click(self, x, y, button, press):
        if press:
            print("Mouse pressed at", x, y, "with button", button)
        else:
            print("Mouse released at", x, y, "with button", button)
        self.button = button
        self.press = press

    def scroll(self, x, y, vertical, horizontal):
        self.scroll_vertical = vertical
        self.scroll_horizontal = horizontal

def expect_pos(pos, size):
    def expect(x, m):
        x = max(0, x)
        x = min(m - 1, x)
        return x
    expected_pos = (expect(pos[0], size[0]), expect(pos[1], size[1]))
    return expected_pos

class Test(TestCase):
    def test_size(self):
        for size in screen_sizes:
            with Display(visible=VISIBLE, size=size):
                mouse = PyMouse()
                eq_(size, mouse.screen_size())

    def test_move(self):
        for size in screen_sizes:
            with Display(visible=VISIBLE, size=size):
                mouse = PyMouse()
                for p in positions:
                    mouse.move(*p)
                    eq_(expect_pos(p, size), mouse.position())

    def test_event(self):
        for size in screen_sizes:
            with Display(visible=VISIBLE, size=size):
                time.sleep(1.0)  # TODO: how long should we wait?
                mouse = PyMouse()
                event = Event()
                event.start()
                # check move
                for p in positions:
                    event.reset()
                    mouse.move(*p)
                    time.sleep(0.01)
                    print('check ', expect_pos(p, size), '=', event.pos)
                    eq_(expect_pos(p, size), event.pos)
                # check buttons
                for btn in buttons:
                    # press
                    event.reset()
                    mouse.press(0, 0, btn)
                    time.sleep(0.01)
                    print("check button", btn, "pressed")
                    eq_(btn, event.button)
                    eq_(True, event.press)
                    # release
                    event.reset()
                    mouse.release(0, 0, btn)
                    time.sleep(0.01)
                    print("check button", btn, "released")
                    eq_(btn, event.button)
                    eq_(False, event.press)
                # check scroll
                def check_scroll(btn, vertical=None, horizontal=None):
                    event.reset()
                    mouse.press(0, 0, btn)
                    time.sleep(0.01)
                    if vertical:
                        eq_(vertical, event.scroll_vertical)
                    elif horizontal:
                        eq_(horizontal, event.scroll_horizontal)
                print("check scroll up")
                check_scroll(4, 1, 0)
                print("check scroll down")
                check_scroll(5, -1, 0)
                print("check scroll left")
                check_scroll(6, 0, 1)
                print("check scroll right")
                check_scroll(7, 0, -1)
                event.stop()
