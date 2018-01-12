"""
core api functionality
===
created by John DeVitis, 2016
"""

from St7API import *
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

beamMaterialData = {
    'modulus':ipBeamModulus,
    'shear':ipBeamShear,
    'poisson':ipBeamPoisson,
    'density':ipBeamDensity,
    'alpha':ipBeamAlpha,
    'viscosity':ipBeamViscosity,
    'damping_ratio':ipBeamDampingRatio,
    'conductivity':ipBeamConductivity,
    'specific_heat':ipBeamSpecificHeat
    }

plateIsoMaterialData = {
    'modulus':ipPlateIsoModulus,
    'poisson':ipPlateIsoPoisson,
    'density':ipPlateIsoDensity,
    'alpha':ipPlateIsoAlpha,
    'viscosity':ipPlateIsoViscosity,
    'damping_ratio':ipPlateIsoDampingRatio,
    'conductivity':ipPlateIsoConductivity,
    'specific_heat':ipPlateIsoSpecificHeat,
    }

plateOrthoMaterialData = {
    'modulus1':ipPlateOrthoModulus1,
    'modulus2':ipPlateOrthoModulus2,
    'modulus3':ipPlateOrthoModulus3,
    'shear12':ipPlateOrthoShear12,
    'shear23':ipPlateOrthoShear23,
    'shear31':ipPlateOrthoShear31,
    'poisson12':ipPlateOrthoPoisson12,
    'poisson23':ipPlateOrthoPoisson23,
    'poisson31':ipPlateOrthoPoisson31,
    'density':ipPlateOrthoDensity,
    'alpha12':ipPlateOrthoAlpha1,
    'alpha23':ipPlateOrthoAlpha2,
    'alpha31':ipPlateOrthoAlpha3,
    'viscosity':ipPlateOrthoViscosity,
    'damping_ratio':ipPlateOrthoDampingRatio,
    'conductivity1':ipPlateOrthoConductivity1,
    'condictivity2':ipPlateOrthoConductivity2,
    'specific_heat':ipPlateOrthoSpecificHeat
    }



class Model(object):
    """Strand7 Model Wrapper"""

    uid = 1
    scratch = 'C:\Temp'
    isopen = False

    def __init__(self, filename='beam1.st7', scratch='C:\Temp', uid=1):
        self.filename = filename
        self.scratch = scratch
        self.uid = uid

    def open(self):
        """open model instance"""
        if not self.isopen:
            chkErr(St7OpenFile(self.uid, self.filename.encode(), self.scratch.encode()))
            self.isopen = True

    def close(self):
        """close model instance"""
        if self.isopen:
            chkErr(St7CloseFile(self.uid))
            self.isopen = False

    def printImage(self,fname='C:\Temp\image00.jpg',width=1920,height=1080):
        chkErr(St7ExportImageFile(self.uid, fname.encode(),itJPEG,width,height))

    def showWindow(self):
        chkErr(St7CreateModelWindow(self.uid))
        chkErr(St7ShowModelWindow(self.uid))
        chkErr(St7PositionModelWindow(self.uid,0,0,640,480))

    def redraw(self):
        chkErr(St7RedrawModel(self.uid,True))

    def destroyWindow(self):
        chkErr(St7DestroyModelWindow(self.uid))

    def totals(self, disp=False):
        """get total bricks, nodes, beams, and plates. returns dictionary"""
        nEnt = ctypes.c_int()
        tots = {}
        if disp: print('Element totals:')
        for k, v in entityTypes.items():
            chkErr(St7GetTotal(self.uid, v, nEnt))
            tots[k] = nEnt.value
            if disp: print('\t\t{}: {}'.format(k, tots[k]))
        return tots


class NFA(object):
    """NFA Solver Wrapper"""

    spectralname = ''
    isopen = False
    isrun = False

    def __init__(self, uid, filename = 'beam1.NFA', logname = 'beam1.NFL',fcase = 1, nsm=(1,),nmodes = 4):
        self.uid = uid
        self.filename = filename
        self.logname = logname
        self.fcase = fcase
        self.nsm = nsm
        self.nmodes = nmodes

    def open(self, combinations = False):
        """opens nfa result file"""
        nprim, nsec = ctypes.c_int(), ctypes.c_int()
        if (self.isrun or os.path.isfile(self.filename)) and not self.isopen:
            chkErr(St7OpenResultFile(self.uid, self.filename.encode(),self.spectralname.encode(), False, nprim, nsec))
            self.isopen = True
        else:
            print('NFA solver not run yet or file not found.')
        return nprim, nsec

    def close(self):
        """closes nfa result file if open"""
        if self.isopen:
            # close result file
            chkErr(St7CloseResultFile(self.uid))
            self.isopen = False
        else:
            print('NFA result file not open.')

    def run(self,disp=False):
        """run natural frequency solver. assumes model file is open. returns the generated nfa result file and nfa result log file"""
        # set up solver defaults
        chkErr(St7SetSolverFreedomCase(self.uid,self.fcase))
        chkErr(St7SetSolverNonlinearGeometry(self.uid, btFalse))
        chkErr(St7SetSolverNonlinearMaterial(self.uid, btFalse))
        chkErr(St7SetSolverTemperatureDependence(self.uid, tdNone))
        chkErr(St7SetEntityResult(self.uid, srElementNodeForce,btTrue))
        chkErr(St7SetSolverDefaultsInteger(self.uid, spFormStiffMatrix, 2))
        # nfa solver and log file names
        chkErr(St7SetResultFileName(self.uid, self.filename.encode()))
        chkErr(St7SetResultLogFileName(self.uid, self.logname.encode()))
        # assign number of modes to calculate
        chkErr(St7SetNFANumModes(self.uid,self.nmodes))
        # enable all desired NSM cases - NSM needs to be a list!
        for m in self.nsm:
            chkErr(St7EnableNFANonStructuralMassCase(self.uid, m))
        # run solver
        chkErr(St7RunSolver(self.uid, stNaturalFrequencySolver, smBackgroundRun, btTrue))
        if disp: print('NFA run finished (uid: {})'.format(self.uid))
        self.isrun = True

    def getResults(self):
        """
        returns the results frequencies and mode shapes.
        """
        # TODO: add option to delete result file after read. will also need to have a check when opening for file ot exist
        # run solver if not done yet
        if not self.isrun: self.run()
        self.open()
        freq = self.getFrequencies()
        U = self.getModeShapes()
        self.close()
        return freq, U

    def getModeShapes(self, nodes=(1,)):
        """
        returns numpy array of size [nnodes, 6dof , nmodes]
        """
        self.open()
        nd = (ctypes.c_double*6)()
        U = np.empty((len(nodes),6,self.nmodes))
        for mode in np.arange(self.nmodes):
            node_count = 0
            for node in nodes:
                chkErr(St7GetNodeResult(self.uid,rtNodeDisp,node,mode+1,nd))
                U[node_count,:,mode] = nd
                node_count += 1
        self.close()
        return U

    def getFrequencies(self, disp=True):
        # get natural frequencies
        self.open()
        frq = ctypes.c_double()
        freq = []
        for mode in range(1,self.nmodes+1):
            chkErr(St7GetFrequency(self.uid,mode,frq))
            freq.append(frq.value)
            if disp: print('Mode {}    Frequency: {} Hz'.format(mode,frq.value))
        # close result file
        self.close()
        return np.array(freq)



class Node(object):
    """Strand7 Node Class"""
    pass



def start():
    """initialize API"""
    chkErr(St7Init())
    print('St7API initialized')


def stop():
    """release API"""
    chkErr(St7Release())
    print('St7API released')


def chkErr(ErrorCode):
    """
    Error checking function. Turns a non-zero integer returned by Strand API call into a Python exception.
    This is pretty much the original that shipped with Strand7
    """
    ErrorOccured = (ErrorCode != 0)
    if ErrorOccured:
        ErrorString = ctypes.create_string_buffer(kMaxStrLen)
        # Attempt to get API error string
        iErr = St7GetAPIErrorString(ErrorCode, ErrorString, kMaxStrLen)
        # If that failed, attempt to retrive a solver error string
        if iErr:
            iErr = St7GetSolverErrorString(ErrorCode, ErrorString, kMaxStrLen)
        if not iErr:
            raise Exception('%s (%d)' % (ErrorString.value, ErrorCode))
        else:
            raise Exception('An unknown error occured (%d)' % ErrorCode)
    return ErrorOccured
