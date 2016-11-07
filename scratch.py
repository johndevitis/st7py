from st7py import core
from st7py.model import Model
#from st7py.solvers import nfa
import csv
from collections import defaultdict

def getAllNodes():
    try:
        # initialize api
        core.start()
        # create model object using path, name, and scratch keyword arguments
        model = Model(path = r'C:\Users\John\repos\st7py\examples\models',
                      name = r'beam1.st7',
                      scratch = r'C:\Temp')
        # open model
        model.open()

        # get dictionary of totals for all elements
        #  set disp=True to print totals
        tots = model.totals(disp=True)

        # get all nodal coordinates
        # note - lists are zero indexed, so coords[0] corresponds to nodeid=1
        coords = model.getNodes(disp=False)

        # natural frequency analysis
        model.runNFA(modes=10)
        freq = model.getFrequency(modes=10)

        # get mode shapes
        U = defaultdict(list)
        for mode in range(1,10+1):
            print('Getting shapes for mode: {}'.format(mode))
            U[mode] = model.getModeShapes(mode=mode)

        return tots, coords, freq, U
    finally:
        model.close()
        core.stop()

def writeResults(coords,freq,U):
    # write shapes to file
    for ent in U:
        with open('dict-test_{}.csv'.format(ent),'w',newline='') as f:
            writer = csv.writer(f)
            for row in U[ent]:
                writer.writerow(row)

    with open('route19-coords.csv','w',newline='') as f:
        writer = csv.writer(f)
        for row in coords:
            writer.writerow(row)

    with open('route19-freqs.csv','w',newline='') as f:
        writer = csv.writer(f)
        for row in freq:
            writer.writerow([row])
