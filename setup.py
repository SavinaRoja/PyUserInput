from distutils.core import setup

setup(name='PyUserInput',
      version='0.1',
      description='A simple, cross-platform module for mouse and keyboard control',
      long_description='''PyUserInput provides cross-platform tools for the
 programmatic fabrication of user input through the mouse and keyboard. Through
 the PyKeyboardEvent and PyMouseEvent classes one can also define event
 handling for detection of user keyboard and mouse input. Mouse support exists
 for Mac, Linux, and Windows. At this time, keyboard support consists of Linux
 and Windows.''',
      author='Paul Barton',
      #Original author of PyMouse: Pepijn de Vos
      author_email='pablo.barton@gmail.com',
      url='https://github.com/SavinaRoja/PyUserInput',
      packages = ['pykeyboard', 'pymouse'],
      license='LICENSE.txt',
      )
