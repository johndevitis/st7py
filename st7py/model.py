"""
model
=====

model wrapper for Strand7 API

jdv 11042016
"""
from st7py import St7API
import ctypes
import os

def start():
    """initialize API"""
    chkErr(St7API.St7Init())
    print('St7API initialized')
    return True

def stop():
    """release API"""
    chkErr(St7API.Release())
    print('St7API released')
    return False

class Model(object):
    """Strand7 Model Class.
    uID is auto incremeted on instantiation of any Model class.
    entityTypes mapping (e.g. St7API.tyNODE: 'Nodes' ) is held as a constant attribute of class Model.
    """

    uID = 0  # auto incremented on instantiation
    started = False
    entityTypes = ((St7API.tyNODE, 'Nodes'),
                   (St7API.tyBEAM, 'Beams'),
                   (St7API.tyPLATE, 'Plates'),
                   (St7API.tyBRICK, 'Bricks'))

    def __init__(self, path=r"C:\Users\John\repos\st7py\examples\models", name=r"beam1.st7", scratch=r"C:\Temp"):

        # advance global class counter
        Model.uID += 1

        # assign global class values to instance
        self.uID = Model.uID

        # self.started = Model.started
        Model.started = start()

        # assign user input & defaults
        self.path = path
        self.name = name
        self.scratch = scratch
        self.opened = False

    def open(self):
        filename = os.path.join(self.path, self.name)
        chkErr(St7API.St7OpenFile(self.uID, filename.encode(), self.scratch.encode()))
        self.opened = True
        print('Model opened.')

    def close(self):
        chkErr(St7API.St7CloseFile(self.uID))
        self.opened = False
        print('Model closed.')

    @property
    def totals(self):
        nEnt = ctypes.c_int()
        entTots = {}
        print('Gathering entity totals...')
        for (entTy, entName) in self.entityTypes:
            chkErr(St7API.St7GetTotal(self.uID, entTy, nEnt))
            entTots[entTy] = nEnt.value
            print(' %s: %d' % (entName, entTots[entTy]))


def chkErr(ErrorCode):
    """
    Error checking function. Turns a non-zero integer returned by Strand API call into a Python exception.
    This is pretty much the original that shipped with Strand7
    """
    ErrorOccured = (ErrorCode != 0)
    if ErrorOccured:
        ErrorString = ctypes.create_string_buffer(St7API.kMaxStrLen)
        # Attempt to get API error string
        iErr = St7API.St7GetAPIErrorString(ErrorCode, ErrorString, St7API.kMaxStrLen)
        # If that failed, attempt to retrive a solver error string
        if iErr:
            iErr = St7API.St7GetSolverErrorString(ErrorCode, ErrorString, St7API.kMaxStrLen)
        if not iErr:
            raise Exception('%s (%d)' % (ErrorString.value, ErrorCode))
        else:
            raise Exception('An unknown error occured (%d)' % ErrorCode)
    return ErrorOccured

"""
def main():
    model = Model()

if __name__ == '__main__':
    main()
"""
