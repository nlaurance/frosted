"""
Implementation of the command-line I{frosted} tool.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from pies.overrides import *

from frosted.api import check, checkPath, checkRecursive, iterSourceCode, main
