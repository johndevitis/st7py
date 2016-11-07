"""
core
===
core api functionality
created by John DeVitis, 11/05/2016
"""
from st7py import St7API
import ctypes

def start():
    """initialize API"""
    chkErr(St7API.St7Init())
    print('St7API initialized')


def stop():
    """release API"""
    chkErr(St7API.St7Release())
    print('St7API released')


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
