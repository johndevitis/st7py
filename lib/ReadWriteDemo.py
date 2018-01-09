# Read/Write Demo

import St7API
import ctypes
import sys

# Different function for entering text between Python 2 and Python 3
if sys.version_info[0] >= 3:
    inFunc = input
else:
    inFunc = raw_input


# Error checking function. Turns a non-zero integer returned by Strand API call into a Python exception
def ChkErr(ErrorCode):
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



# Main program code. Use try...finally syntax to ensure the API is released even in the case of an expection.
try:
    St7API.St7Init()

    # 'encode' function return bytes from string in Python 3.
    fileToOpen = inFunc('Enter file path: ').encode()
    ChkErr(St7API.St7OpenFile(1, fileToOpen, r'c:\temp'.encode()))

    # Display the model title and author
    modTitle, modAuth = ctypes.create_string_buffer(St7API.kMaxStrLen), ctypes.create_string_buffer(St7API.kMaxStrLen)
    ChkErr(St7API.St7GetTitle(1, St7API.TITLEModel, modTitle, St7API.kMaxStrLen))
    ChkErr(St7API.St7GetTitle(1, St7API.TITLEAuthor, modAuth, St7API.kMaxStrLen))
    print('Title:  ' + modTitle.value.decode())
    print('Author: ' + modAuth.value.decode())

    # Retrive and display the number of elements in the model
    EntTypes = ((St7API.tyNODE, 'Nodes'),
                (St7API.tyBEAM, 'Beams'),
                (St7API.tyPLATE, 'Plates'),
                (St7API.tyBRICK, 'Bricks'))

    nEnt = ctypes.c_int()
    entTots = {}
    print('Entity Totals')
    for (entTy, entName) in EntTypes:
        #ChkErr(St7API.St7GetTotal(1, entTy, nEnt))
        ChkErr(St7API.St7GetTotal(1, entTy, nEnt))
        entTots[entTy] = nEnt.value
        print(' %s: %d' % (entName, entTots[entTy]))

    # Retrive and display the coordinates of the frist few nodes in the mesh
    XYZType = ctypes.c_double * 3
    XYZ = XYZType()
    maxNodes = min( (10, entTots[St7API.tyNODE]) )
    print('Coordinates of first {0} nodes:'.format(maxNodes))
    for iNode in range(1, maxNodes+1):
        ChkErr(St7API.St7GetNodeXYZ(1, iNode, XYZ))
        print(' Node {iN}: ( {X}, {Y}, {Z} )'.format(iN=iNode, X=XYZ[0], Y=XYZ[1], Z=XYZ[2]))
        

    # Update some nodal coordinates based on the contents of a text file
    nodeCoordFile = inFunc('Full path to nodal coordinate file: ').encode()
    with open(nodeCoordFile) as newNodeCoords:
        print('Assigning nodal coordinates from {0}'.format(nodeCoordFile.decode()))
        for line in newNodeCoords:
            splitLine = line.split()
            iNode, XYZ[0], XYZ[1], XYZ[2] = int(splitLine[0]), float(splitLine[1]), float(splitLine[2]), float(splitLine[3])
            print(' Setting node {iN} coordinates to ( {X}, {Y}, {Z} )'.format(iN=iNode, X=XYZ[0], Y=XYZ[1], Z=XYZ[2]))
            ChkErr(St7API.St7SetNodeXYZ(1, iNode, XYZ))
    
    print('Saving and closing ' + fileToOpen.decode())
    ChkErr(St7API.St7SaveFile(1))
    
finally:
    St7API.St7Release()
