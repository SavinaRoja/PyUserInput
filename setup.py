from distutils.core import setup

def long_description():
    with open('README.md', 'r') as readme:
        readme_text = readme.read()
    return(readme_text)

setup(name='PyUserInput',
      version='0.1.1',
      description='A simple, cross-platform module for mouse and keyboard control',
      long_description=long_description(),
      author='Paul Barton',
      #Original author of PyMouse: Pepijn de Vos
      author_email='pablo.barton@gmail.com',
      url='https://github.com/SavinaRoja/PyUserInput',
      packages = ['pykeyboard', 'pymouse'],
      license='http://www.gnu.org/licenses/gpl-3.0.html',
      keywords='mouse keyboard user input event'
      )
