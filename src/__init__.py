# src/__init__.py
"""
Root package initialization for the SMS Sender application.
This file marks the src directory as a Python package and can contain package-level configurations.
"""
from . import gui
from . import services
from . import utils

__version__ = '0.1.0'
__author__ = 'Gavin Berryman'
__email__ = 'gavin@iovox.com'

__all__ = ['gui', 'services', 'utils']
