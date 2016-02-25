PyUserInput
===========

**PyUserInput is a group project so we've moved the project over to a group
organization: https://github.com/PyUserInput/PyUserInput . That is now the
active development repository and I'll be phasing this one out, so please go
there for the latest code and to post new issues. This should be corrected on
PyPI in the next version update of PyUserInput.**

A module for cross-platform control of the mouse and keyboard in python that is
simple to use.

Mouse control should work on Windows, Mac, and X11 (most Linux systems).
Scrolling is implemented, but users should be aware that variations may
exist between platforms and applications.

Keyboard control works on X11(linux) and Windows systems. Mac control is a work
in progress.

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

PyKeyboard allows for a range of ways for sending keystrokes:

    # pressing a key
    k.press_key('H')
    # which you then follow with a release of the key
    k.release_key('H')
    # or you can 'tap' a key which does both
    k.tap_key('e')
    # note that that tap_key does support a way of repeating keystrokes with a interval time between each
    k.tap_key('l',n=2,interval=5) 
    # and you can send a string if needed too
    k.type_string('o World!')
    

and it supports a wide range of special keys:

    #Create an Alt+Tab combo
    k.press_key(k.alt_key)
    k.tap_key(k.tab_key)
    k.release_key(k.alt_key)
    
    k.tap_key(k.function_keys[5])  # Tap F5
    k.tap_key(k.numpad_keys['Home'])  # Tap 'Home' on the numpad
    k.tap_key(k.numpad_keys[5], n=3)  # Tap 5 on the numpad, thrice

Note you can also send multiple keystrokes together (e.g. when accessing a keyboard shortcut) using the press_keys method:

    # Mac example
    k.press_keys(['Command','shift','3'])
    # Windows example
    k.press_keys([k.windows_l_key,'d'])

Consistency between platforms is a big challenge; Please look at the source for the operating system that you are using to help understand the format of the keys that you would need to send. For example:

    # Windows
    k.tap_key(k.alt_key)
    # Mac
    k.tap_key('Alternate')

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

These are a few things I am considering for future development in
PyUserInput:

 * Ensuring that PyMouse capturing works for all platforms
 * Implement PyKeyboard capturing (add PyKeyboardEvent for Mac as well)
 * PyMouse dynamic delta scrolling (available in Mac and Windows, hard to standardize)
 * Make friends with more Mac developers, testing help is needed...


Many thanks to
--------------

[Pepijn de Vos](https://github.com/pepijndevos) - For making
[PyMouse](https://github.com/pepijndevos/PyMouse) and allowing me to modify
and distribute it along with PyKeyboard.

[Jack Grigg](https://github.com/pythonian4000) - For contributions to
cross-platform scrolling in PyMouse.
