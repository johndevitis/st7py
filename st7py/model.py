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
import numpy as np

# api helpers
entityTypes = {
    'Nodes':tyNODE,
    'Beams':tyBEAM,
    'Plates': tyPLATE,
    'Bricks':tyBRICK,
    }

unitTypes = {
    'Length':ipLENGTHU,
    'Force':ipFORCEU,
    'Stress':ipSTRESSU,
    'Mass':ipMASSU,
    'Temperature':ipTEMPERU,
    'Energy':ipENERGYU,
    }

unitMap = {'Length':['m','cm','mm','ft','in'],
           'Force':['N','kN','MN','kilo-force','lbf','ton-force','kip-force'],
           'Stress':['Pa','kPa','MPa','KSCm','psi','ksi','psf'],
           'Mass':['kg','ton','g','lb','slug'],
           'Temperature':['C','F','K'],
           'Energy':['joule','btu','ftlbf','calorie'],
           }


class Model(object):
    """Strand7 Model Class.
    uID is auto incremeted on instantiation of any Model class.
    entityTypes mapping (e.g. tyNODE: 'Nodes' ) is held as a constant attribute of class Model.
    """
    uID = 0  # auto incremented on instantiation

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
        """ full path + name + ext """
        return os.path.join(self.path,self.name)

    @property
    def _fullname(self):
        """ encoded fullname """
        return self.fullname.encode()
    @property
    def _scratch(self):
        """ encoded scratch path """
        return self.scratch.encode()


    def open(self):
        """open model instance"""
        chkErr(St7OpenFile(self.uID, self._fullname, self._scratch))
        self.opened = True
        print('Model opened.')


    def close(self):
        """close model instance"""
        chkErr(St7CloseFile(self.uID))
        self.opened = False
        print('Model closed.')


    def totals(self, disp=True):
        """get total bricks, nodes, beams, and plates. returns dictionary"""
        nEnt = ctypes.c_int()
        entityTotals = {}
        if disp: print('\tEntity totals:')
        for k, v in entityTypes.items():
            chkErr(St7GetTotal(self.uID, v, nEnt))
            entityTotals[k] = nEnt.value
            if disp: print('\t\t{}: {}'.format(k, entityTotals[k]))
        return entityTotals


    def getNodes(self, disp=True):
        """get all nodal coordinates in model"""

        # get numeric type of x, y, z coordinates
        tots = self.totals(disp=False)
        nodes = tots['Nodes']

        # initialize list (to append to) and st7 double input
        coords = []
        coord = (ctypes.c_double*3)()

        # loop with 1 index (instead of  typical 0)
        # also note - need to slice the coord array to produce a copy
        for node in range(1, nodes+1):
            chkErr(St7GetNodeXYZ(self.uID, node, coord))
            coords.append(coord[:])
            if disp:  # print output if desired
                print('Node: {id} {x}, {y}, {z}'.format(id=node, x=coord[0],  y=coord[1], z=coord[2]))
        return coords


    def showWindow(self):
        chkErr(St7CreateModelWindow(self.uID))
        chkErr(St7ShowModelWindow(self.uID))
        chkErr(St7PositionModelWindow(self.uID,0,0,640,480))

    def redraw(self):
        chkErr(St7RedrawModel(self.uID,True))

    def destroyWindow(self):
        chkErr(St7DestroyModelWindow(self.uID))

    def printImage(self,name='C:\Temp\image00.jpg',width=1920,height=1080):
        chkErr(St7ExportImageFile(self.uID, name.encode(),itJPEG,width,height))


    def _setResultFileName(self):
        """ strips the extension off of the base model name and sets the result file w/o extension (from Strand7 PlateDemo.py exmaple)"""
        resFileName = self._getResFile()
        chkErr(St7SetResultFileName(self.uID,resFileName))

    def _getResFile(self):
        """ strips extension off of (encoded) fullname"""
        # note: self._fullname is already encoded
        return os.path.splitext(self._fullname)[0]

    def _chkString(self, name):
        """ _chkString not tested yet"""
        if isinstance(name, str):
            return name.encode()
        elif isinstance(name, bytes):
            return name
        else:
            print('you messed up.')

    def _closeResultFile(self):
        chkErr(St7CloseResultFile(self.uID))




    def runNFA(self, modes=5):
        # set up result file name
        resName = os.path.splitext(self._fullname)[0] + '.nfa'.encode()
        # set number of modes to calculate
        chkErr(St7SetNFANumModes(self.uID, modes))
        # run solver
        chkErr(St7RunSolver(self.uID, stNaturalFrequencySolver, smBackgroundRun, btTrue))

    def getModeShapes(self, mode=1):
        # open result file
        resName = os.path.splitext(self._fullname)[0] + '.nfa'.encode()
        nPrim, nSec = ctypes.c_int(), ctypes.c_int()
        chkErr(St7OpenResultFile(self.uID,resName,''.encode(),False,nPrim,nSec))
        nd = (ctypes.c_double*6)()
        tots = self.totals(disp=False)
        nodes = tots['Nodes']
        u = []
        for node in range(1,nodes+1):
            chkErr(St7GetNodeResult(self.uID,rtNodeDisp,node,mode,nd))
            u.append(nd[:])
        # close result file
        chkErr(St7CloseResultFile(self.uID))
        return u

    def getFrequency(self, modes=5):

        # open result file
        resName = os.path.splitext(self._fullname)[0] + '.nfa'.encode()
        nPrim, nSec = ctypes.c_int(), ctypes.c_int()
        chkErr(St7OpenResultFile(self.uID,resName,''.encode(),False,nPrim,nSec))

        # get natural frequencies
        frq = (ctypes.c_double)()
        freq = []
        for mode in range(1,modes+1):
            chkErr(St7GetFrequency(self.uID, mode,frq))
            freq.append(frq.value)
            print('Frequencies: {}'.format(frq))

        # close result file
        chkErr(St7CloseResultFile(self.uID))

        return freq
