"""
st7py
=====

Strand7 API. In Python this time.

Created by John DeVitis, johndevitis@gmail.com
"""

import sys
from os.path import dirname

#from st7py.model import Model

# package info
__package_name__ = 'st7py.py'
__title__ = 'st7py'
__version__ = '0.0.1'
__author__ = 'John DeVitis'
__author_email__ = 'johndevitis@gmail.com'
__license__ = 'MIT'
__url__ = 'http://github.com/johndevitis/st7py'


# find and save base calling directory
st7py_base_dir = dirname(sys.modules[__name__].__file__)
