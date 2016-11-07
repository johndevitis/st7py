from st7py import core
from st7py.model import Model

try:
    core.start()
    model = Model(path = r'C:\Users\John\repos\st7py\examples\models',
                  name = r'beam1.st7',
                  scratch = r'C:\Temp')
    model.open()
    tots = model.totals()

    model.getNodeCoords()
    #model.runNFA(2)


finally:
    model.close()
    core.stop()
