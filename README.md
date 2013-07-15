PyUserInput
===========

A module for cross-platform control of the mouse and keyboard in python that is
simple to use.

Mouse control should work well for most users on Windows, Mac, and X11 (most
linux) systems.

Keyboard control works on X11(linux) and Windows systems. Mac control is
partially complete.

Dependencies
------------

Depending on your platform, you will need the following python modules for
PyUserInput to function:

  * Linux - Xlib
  * Mac - Quartz, AppKit
  * Windows - pywin32, pyHook

How to get started
------------------

After installing PyUserInput, you should have pymouse and pykeyboard modules in
your python path. Let's make a mouse and keyboard object:

    from pymouse import PyMouse
    from pykeyboard import PyKeyboard
    
    m = PyMouse()
    k = PyKeyboard()

Here's an example of clicking the center of the screen and typing "Hello, World!":

    x_dim, y_dim = m.screen_size()
    m.click(x_dim/2, y_dim/2, 1)
    k.type_string('Hello, World!')

I'll be working on a more complete documentation later, but most of the
functionality should be evident in the source.

I'd like to make a special note about using PyMouseEvent and PyKeyboardEvent.
These objects are a framework for listening for mouse and keyboard input; they
don't do anything besides listen until you subclass them. I'm still formalizing
PyKeyboardEvent, so here's an example of subclassing PyMouseEvent:

    from pymouse import PyMouseEvent

    def fibo():
        a = 0
        yield a
        b = 1
        yield b
        while True:
            a, b = b, a+b
            yield b

    class Clickonacci(PyMouseEvent):
        def __init__(self):
            PyMouseEvent.__init__(self)
            self.fibo = fibo()

        def click(self, x, y, button, press):
            '''Print Fibonacci numbers when the left click is pressed.'''
            if button == 1:
                if press:
                    print(self.fibo.next())
            else:  # Exit if any other mouse button used
                self.stop()

    C = Clickonacci()
    C.run()

Intended Functionality of Capturing in PyUserInput
--------------------------------------------------

For PyMouseEvent classes, the variables "capture" and "capture_move" may be
passed during instantiation. If `capture=True` is passed, the intended result
is that all mouse button input will go to your program and nowhere else. The
same is true for `capture_move=True` except it deals with mouse pointer motion
instead of the buttons. Both may be set simultaneously, and serve to prevent
events from propagating further. If you notice any bugs with this behavior,
please bring it to our attention.

A Short Todo List
-----------------

These are a few things I am considering for the near future development in
PyUserInput:

 * Ensuring that PyMouse capturing works for all platforms
 * Implement PyKeyboard capturing (add PyKeyboardEvent for Mac as well)
 * Provide a unified interface for "scrolling" in PyMouse


Many thanks to
--------------

Pepijn de Vos - For making [PyMouse](https://github.com/pepijndevos/PyMouse)
and allowing me to modify and distribute it along with PyKeyboard.
