"""
AIinDigitalBank Package Initialization
"""

__version__ = "1.0.0"
__author__ = "Tuan Tran"
__email__ = "tuantranscientist@gmail.com"
__description__ = "AI-Driven Digital Banking Platform"

# Expose main modules
from . import models
from . import data
from . import api

__all__ = [
    "models",
    "data",
    "api"
]
