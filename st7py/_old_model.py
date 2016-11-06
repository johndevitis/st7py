"""
model
=====

model wrapper for Strand7 API

jdv 11042016
"""
#from st7py import St7API
from st7py.St7API import *
from st7py.core import chkErr
import ctypes
import os
import sys

class Model(object):
    """Strand7 Model Class.
    uID is auto incremeted on instantiation of any Model class.
    entityTypes mapping (e.g. St7API.tyNODE: 'Nodes' ) is held as a constant attribute of class Model.
    """

    uID = 0  # auto incremented on instantiation

    entityTypes = ((St7API.tyNODE, 'Nodes'),
                   (St7API.tyBEAM, 'Beams'),
                   (St7API.tyPLATE, 'Plates'),
                   (St7API.tyBRICK, 'Bricks'))

    def __init__(self, path=r"C:\Users\John\repos\st7py\examples\models", name=r"beam1.st7", scratch=r"C:\Temp"):
        # advance global class counter
        Model.uID += 1
        # assign global class values to instance
        self.uID = Model.uID
        # assign user input & defaults
        self.path = path
        self.name = name
        self.scratch = scratch


    def open(self):
        filename = os.path.join(self.path, self.name)
        chkErr(St7API.St7OpenFile(self.uID, self._fullname, self._scratch))
        self.opened = True
        print('Model opened.')


    def close(self):
        chkErr(St7API.St7CloseFile(self.uID))
        self.opened = False
        print('Model closed.')


    @property
    def fullname(self):
        return os.path.join(self.path,self.name)

    @property
    def _fullname(self):
        return self.fullname.encode()
    @property
    def _scratch(self):
        return self.scratch.encode()

    def totals(self):
        nEnt = ctypes.c_int()
        entTots = {}
        print('Gathering entity totals...')
        for (entTy, entName) in self.entityTypes:
            chkErr(St7API.St7GetTotal(self.uID, entTy, nEnt))
            entTots[entTy] = nEnt.value
            print(' %s: %d' % (entName, entTots[entTy]))


    def showWindow(self):
        chkErr(St7API.St7CreateModelWindow(1))
        chkErr(St7API.St7ShowModelWindow(1))
        chkErr(St7API.St7PositionModelWindow(1,0,0,640,480))

    def runLSA(self):
        chkErr(St7API.St7RunSolver(1, stLinearStaticSolver, smBackgroundRun, 1))
