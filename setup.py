try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os
import sys


def long_description():
    readme = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme, 'r') as inf:
        readme_text = inf.read()
    return(readme_text)

setup(name='PyUserInput',
      version='0.1.9',
      description='A simple, cross-platform module for mouse and keyboard control',
      long_description=long_description(),
      author='Paul Barton',
      #Original author of PyMouse: Pepijn de Vos
      author_email='pablo.barton@gmail.com',
      url='https://github.com/SavinaRoja/PyUserInput',
      package_dir = {'': '.'},
      packages = ['pykeyboard', 'pymouse'],
      license='http://www.gnu.org/licenses/gpl-3.0.html',
      keywords='mouse,keyboard user input event',
      )

def dependency_check(dep_list):
    for dep in dep_list:
        try:
            __import__(dep)
        except ImportError:
            print('Missing dependency, could not import this module: {0}'.format(dep))

#Check for dependencies
if sys.platform == 'darwin':  # Mac
    dependency_check(['Quartz', 'AppKit'])
elif sys.platform == 'win32':  # Windows
    dependency_check(['win32api', 'win32con', 'pythoncom', 'pyHook'])
else:  # X11 (LInux)
    dependency_check(['Xlib'])
