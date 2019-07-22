
import numpy as np
from .. import Constants as Cst
from . import AtomIO

class Atom:

    def __init__(self, _filepath):
        r"""
        initial method of class Atom.

        Parameters
        ----------

        _filepath : str
            path (and filename) to
        """

        self.filepath = filepath


    def __read_Level(self):
        r"""
        restore the Level information from
        """
