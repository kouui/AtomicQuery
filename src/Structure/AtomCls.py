
import numpy as np
from .. import Constants as Cst
from . import AtomIO

class Atom:

    def __init__(self, _filepath, _file_Aji=None, _file_CEe=None, _file_CEp=None):
        r"""
        initial method of class Atom.

        Parameters
        ----------

        _filepath : str
            path (and filename) to config file *.Level

        _file_Aji : str
            path (and filename) to Aji data file *.Aji, default: None

        _file_CEe : str
            path (and filename) to Electron impact Effective Collisional Strength data file *.Electron, default: None

        _file_CEp : str
            path (and filename) to Proton impact Effective Collisional Strength data file *.Proton, default: None
        """
        self.filepath_dict = {
            "config" : _filepath,

        }
        self.__read_Level()
        self.__make_line_idx_ctj_table()

        # whether to read *.Aji file at __init__
        if _file_Aji is not None:
            self.read_Aji(_file_Aji)

        # whether to read *.Electron and *.Proton files at __init__
        if _file_CEe is not None:
            self.read_CE(_file_CEe, _file_CEp)


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

    def read_Aji(self, _path):
        r"""
        read Aji information from *.Aji

        Parameters
        ----------

        _path : str
            path to *.Aji data file
        """

        print("Reading Einstein Aji coefficient from : \n", _path)
        print("...")

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
        del idx    # for safety
        self.Line.AJI[:] = 0

        AtomIO.read_line_info(_lns=fLines, _Aji=self.Line.AJI[:], _line_ctj_table=self.Line_ctj_table)

        # calculate f0, w0, w0_AA
        for k in range(self.nLine):
            i = self.Line.idxI[k]
            j = self.Line.idxJ[k]
            self.Line.f0[k] = (self.Level.erg[j]-self.Level.erg[i]) / Cst.h_
        self.Line.w0[:] = Cst.c_ / self.Line.f0[:]
        self.Line.w0_AA[:] = self.Line.w0[:] * 1E+8

        print("Finished.")
        print()

    def read_CE(self, _path_electron, _path_proton=None):
        r"""
        read Collisional Excitation table from *.Electron and *.Proton
        in most case the data is Effective Collisional Strength (ECS)

        Parameters
        ----------

        _path_electron : str
            path to *.Electron data file

        _path_proton : str
            path to *.proton
        """
        #---------------------------------------------------------------------
        # read Electron impact data
        #---------------------------------------------------------------------
        print("Reading Electron impact Effective Collisional Strength from : \n", _path_electron)
        print("...")

        self.filepath_dict["CE_electron"] = _path_electron
        with open(_path_electron, 'r') as file:
            fLines = file.readlines()

        # read Temperature grid for interpolation
        rs, nTe, Te, self.CE_type = AtomIO.read_CE_Temperature(_lns=fLines)
        self.CE_Te_table = np.array(Te, dtype=np.double)
        self.CE_table = np.zeros((self.nLine, nTe), dtype=np.double)
        dtype  = np.dtype([
                          ('idxI',np.uint8),      #: level index, the Level index of lower level
                          ('idxJ',np.uint8),      #: level index, the Level index of lower level
                          ('f1',np.uint8),        #: a factor for ESC calculation due to fine structure, \Omega * f1 / f2
                          ('f2',np.uint8),        #: a factor for ESC calculation due to fine structure, \Omega * f1 / f2
                          ('gi',np.uint8),        #: statistical weight of lower level
                          ('gj',np.uint8),        #: statistical weight of upper level
                          ('dEij',np.double)      #: excitation energy, [:math:`erg`]
                          ])

        self.CE_coe = np.recarray(self.nLine, dtype=dtype)

        # idxI and idxJ
        idx = 0
        for i in range(0, self.nLevel):
            for j in range(i+1, self.nLevel):
                self.CE_coe.idxI[idx], self.CE_coe.idxJ[idx] = i, j
                idx += 1
        del idx    # for safety

        # read CE_table
        AtomIO.read_CE_table(_rs=rs, _lns=fLines, _CE_table=self.CE_table,
                _f1=self.CE_coe.f1[:], _f2=self.CE_coe.f2[:], _line_ctj_table=self.Line_ctj_table)

        print("Finished.")
        print()

        #---------------------------------------------------------------------
        # read Proton impact data (not yet imported)
        #---------------------------------------------------------------------
        if _path_proton is not None:

            print("Reading Proton impact Effective Collisional Strength from : \n", _path_proton)
            print("...")
            print("Finished.")
            print()

            self.filepath_dict["CE_proton"] = _path_proton
            with open(_path_proton, 'r') as file:
                fLines = file.readlines()

            pass

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
