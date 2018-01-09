PYTHON
==============================================================================

Two example programs are included to demonstrate the use of the Strand7 API.

The first example "Read Write Demo", demonstrates some reading and writing of
data. A model is opened and strings from Summary->Information are returned.
Entity totals are iterated over, displayed and stored using a tuple and a
dictionary. The program reports the coordinates of the first 10 nodes then
updates nodal coordinates using data found in a file of format
"NodeNumber X Y Z".

The second example "Plate Optimisation", is a demonstration of a basic fully
stressed design method. It is applied to plane stress plate models by varying
the thickness of each plate in an effort to make the von Mises stress field as
uniform as possible. To use the program, you must have a model that only
consists of plane stress plate elements, restraints and an applied force (such
as node forces). Ensure that the model includes appropriate plate property
data. The function RunPlateDemo contains the fundamental code. If the module
is run directly (rather than being imported) a graphical user interface is
presented allowing the user to supply arguments to this function
automatically. The linear static solver is run and Von Mises stress quantities
are retrieved. Based on these results, the thickness of each plate is
modified. A sample model "PlateOptimisation.st7" of a cantilever is included.
The optimisation is run a predefined number of times and results of each
iteration are shown. The model window can be drawn so the user can monitor the
model as it is updated. The program requires that the Tcl/Tk option was
selected on Python's install.

These examples have been developed and tested using Python 2.7 through
Python 3.3 and will only run using 32-bit versions of Python.
==============================================================================


PYTHON
==============================================================================

The following interface file is provided for 32-bit versions of Python:

  - Python\St7API.py

To use this module in your code, the module must be imported as follows:

  import St7API

The API-Python interface has been tested with the following versions of
Python:

  - Python 2.6, 32-bit (Intel)
  - Python 2.7, 32-bit (Intel)
  - Python 3.0, 32-bit (Intel)
  - Python 3.1, 32-bit (Intel)
  - Python 3.2, 32-bit (Intel)
  - Python 3.3, 32-bit (Intel)

Please note that ST7API.DLL is 32-bit and can only be used by 32-bit versions
of Python. To confirm you have a suitable version ensure Python interpreter
reports "32 bit (Intel)" rather than "64 bit (AMD64)" on startup.

==============================================================================
