from st7py import core
from st7py.model import Model
core.start()

model = Model(path = r'C:\Users\John\repos\st7py\examples\models',
              name = r'beam1.st7',
              scratch = r'C:\Temp')

model.open()


model.close()
core.stop()
