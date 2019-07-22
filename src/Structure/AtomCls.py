
import numpy as np
from .. import Constants as Cst
from . import AtomIO

class Atom:

    def __init__(self, _filepath, _file_Aji=None):
        r"""
        initial method of class Atom.

        Parameters
        ----------

        _filepath : str
            path (and filename) to config file *.Level
        """
        self.filepath_dict = {
            "config" : _filepath,

        }
        self.__read_Level()
        self.__make_line_idx_ctj_table()

        if _file_Aji is not None:
            self.read_Aji_info(_file_Aji)


    def __read_Level(self):
        r"""
        read the Level information from config file *.Level
        """

        with open(self.filepath_dict["config"], 'r') as file:
            fLines = file.readlines()

        #--- read general info
        rs, self.Title, self.Z, self.Element, self.nLevel = AtomIO.read_general_info(_rs=0, _lns=fLines)
        self.nLine = self.nLevel * (self.nLevel-1) // 2

        #--- read Level info
        dtype  = np.dtype([
                          ('erg',np.double),            #: level energy, erg
                          ('g',np.uint8),               #: g=2J+1, statistical weight
                          ('stage',np.uint8),           #: ionization stage
                          ])
        self.Level = np.recarray(self.nLevel, dtype=dtype)
        self.Level_info = {"configuration" : [], "term" : [], "J": [], "2S+1": []}
        rs = AtomIO.read_level_info(rs, _lns=fLines, _Level_info=self.Level_info,
                            _erg=self.Level.erg[:], _g=self.Level.g[:], _stage=self.Level.stage[:])
        self.Level.erg[:] *= Cst.eV2erg_

        #--- make tuple of tuple (configuration, term, J)
        self.Level_info_table = []
        for k in range(self.nLevel):
            self.Level_info_table.append((self.Level_info["configuration"][k],
                                          self.Level_info["term"][k],
                                          self.Level_info["J"][k]))
        self.Level_info_table = tuple(self.Level_info_table)

    def __make_line_idx_ctj_table(self):
        r"""
        make a hash dictionary for mapping

        (ctj_i, ctj_j) --> (idxI, idxJ)
        """

        Line_idx_table = []
        Line_ctj_table = []
        for i in range(0, self.nLevel):
            for j in range(i+1, self.nLevel):
                # i : lower level
                # j : upper level
                Line_idx_table.append( ( i, j ) )
                Line_ctj_table.append( ( self.Level_info_table[i], self.Level_info_table[j] ) )

        self.Line_idx_table = tuple( Line_idx_table )
        self.Line_ctj_table = tuple( Line_ctj_table )

    def read_Aji_info(self, _path):
        r"""
        read Aji information from *.Aji
        """

        self.filepath_dict["Aji"] = _path
        with open(_path, 'r') as file:
            fLines = file.readlines()

        #--- read line info
        dtype = np.dtype([('idxI',np.uint16),           #: level index, the Level index of lower level
                           ('idxJ',np.uint16),          #: level index, the Level index of lower level
                           ('AJI',np.double),           #: Einstein Aji coefficient
                           ('f0',np.double),            #: central frequency
                           ('w0',np.double),            #: central wavelength in cm
                           ('w0_AA',np.double),         #: central wavelength in Angstrom
                           ])
        self.Line = np.recarray(self.nLine, dtype=dtype)
        # idxI and idxJ
        idx = 0
        for i in range(0, self.nLevel):
            for j in range(i+1, self.nLevel):
                self.Line.idxI[idx], self.Line.idxJ[idx] = i, j
                idx += 1
        self.Line.AJI[:] = 0

        line_count = AtomIO.read_line_info(_lns=fLines, _Aji=self.Line.AJI[:], _line_ctj_table=self.Line_ctj_table)

        # calculate f0, w0, w0_AA
        for k in range(self.nLine):
            i = self.Line.idxI[k]
            j = self.Line.idxJ[k]
            self.Line.f0[k] = (self.Level.erg[j]-self.Level.erg[i]) / Cst.h_
        self.Line.w0[:] = Cst.c_ / self.Line.f0[:]
        self.Line.w0_AA[:] = self.Line.w0[:] * 1E+8


    def ctj_to_level_idx(self, ctj):
        r"""
        ctj --> idx
        """

        return self.Level_info_table.index(ctj)

    def level_idx_to_ctj(self, idx):
        r"""
        idx --> ctj
        """

        return self.Level_info_table[idx]

    def line_ctj_to_line_idx(self, line_ctj):
        r"""
        (ctj_i, ctj_j) --> (idxI, idxJ)
        """

        return self.Line_idx_table[ self.Line_ctj_table.index( line_ctj ) ]

    def line_idx_to_line_ctj(self, line_idx):
        r"""
        (idxI, idxJ) --> (ctj_i, ctj_j)
        """

        return self.Line_ctj_table[ self.Line_idx_table.index( line_idx ) ]

    def line_index_to_line_ctj(self, _index):
        r"""
        line index (line No.) --> (ctj_i, ctj_j)
        """

        return self.Line_ctj_table[_index]

    def line_ctj_to_line_index(self, line_ctj):
        r"""
        (ctj_i, ctj_j) --> line index (line No.)
        """

        return self.Line_ctj_table.index(line_ctj)

    def line_index_to_line_idx(self, _index):
        r"""
        line index (line No.) --> (idxI, idxJ)
        """

        return self.Line_idx_table[_index]

    def line_idx_to_line_index(self, line_idx):
        r"""
        (idxI, idxJ) --> line index (line No.)
        """

        return self.Line_idx_table.index(line_idx)
