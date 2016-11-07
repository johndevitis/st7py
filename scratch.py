from st7py import core
from st7py.model import Model

def execute():
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
        tots = model.totals()

        # get all nodal coordinates
        # note - lists are zero indexed, so coords[0] corresponds to nodeid=1
        coords = model.getNodes()

        return tots, coords


    finally:
        model.close()
        core.stop()
