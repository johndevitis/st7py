from st7py import core
from st7py.model import Model
#from st7py.solvers import nfa



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
        model.runNFA(nmodes=5)

        freq = model.getFrequency(nmodes=5)

        return tots, coords, freq


    finally:
        model.close()
        core.stop()
