from st7py import core
from st7py.model import Model
#from st7py.solvers import nfa



def getAllNodes():
    try:
        # initialize api
        core.start()
        # create model object using path, name, and scratch keyword arguments
        model = Model(path = r'C:\Users\John\repos\brp\0705151\Models\Apriori',
                      name = r'LiftSpan_apriori.st7',
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
        model.runNFA(nmodes=3)

        freq = model.getFrequency(nmodes=3)

        return tots, coords, freq


    finally:
        model.close()
        core.stop()
