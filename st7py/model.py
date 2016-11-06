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
    entityTypes mapping (e.g. tyNODE: 'Nodes' ) is held as a constant attribute of class Model.
    """

    uID = 0  # auto incremented on instantiation

    entityTypes = ((tyNODE, 'Nodes'),
                   (tyBEAM, 'Beams'),
                   (tyPLATE, 'Plates'),
                   (tyBRICK, 'Bricks'))

    def __init__(self, path=r"C:\Users\John\repos\st7py\examples\models", name=r"beam1.st7", scratch=r"C:\Temp"):
        # advance global class counter
        Model.uID += 1
        # assign global class values to instance
        self.uID = Model.uID
        # assign user input & defaults
        self.path = path
        self.name = name
        self.scratch = scratch

    @property
    def fullname(self):
        return os.path.join(self.path,self.name)

    @property
    def _fullname(self):
        return self.fullname.encode()
    @property
    def _scratch(self):
        return self.scratch.encode()


    def open(self):
        filename = os.path.join(self.path, self.name)
        chkErr(St7OpenFile(self.uID, self._fullname, self._scratch))
        self.opened = True
        print('Model opened.')


    def close(self):
        chkErr(St7CloseFile(self.uID))
        self.opened = False
        print('Model closed.')


    def totals(self):
        nEnt = ctypes.c_int()
        entTots = {}
        print('Entity totals:')
        for (entTy, entName) in self.entityTypes:
            chkErr(St7GetTotal(self.uID, entTy, nEnt))
            entTots[entTy] = nEnt.value
            print(' %s: %d' % (entName, entTots[entTy]))


    def getXYZ(self):
        # get numeric type of coordinates
        coordsType = ctypes.c_double * 3
        coords = coordsType()

        #for nodes in range(self.totals['Nodes'])


    def showWindow(self):
        chkErr(St7CreateModelWindow(self.uID))
        chkErr(St7ShowModelWindow(self.uID))
        chkErr(St7PositionModelWindow(self.uID,0,0,640,480))

    def redraw(self):
        chkErr(St7RedrawModel(self.uID,True))

    def destroyWindow(self):
        chkErr(St7DestroyModelWindow(self.uID))

    def runLSA(self):
        # set results file name to model name without extension
        resName = os.path.splitext(self._fullname)[0]
        chkErr(St7SetResultFileName(self.uID, resFileName))
        # run solver
        chkErr(St7RunSolver(self.uID, stLinearStaticSolver, smBackgroundRun, 1))
