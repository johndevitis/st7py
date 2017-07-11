from st7py import core
from st7py.model import Model
#from st7py.solvers import nfa
import csv
from collections import defaultdict
from multiprocessing import Pool, TimeoutError
from itertools import repeat
import time
import timeit

def execute(path,name,scratch):
    try:

        # create model object
        model = Model(path,name,scratch)

        print(model.uID)

        # open model
        model.open()
        print('opened model')

        # get dictionary of totals for all elements
        #  set disp=True to print totals
        tots = model.totals(disp=True)

        # get all nodal coordinates
        # note - lists are zero indexed, so coords[0] corresponds to nodeid=1
        coords = model.getNodes(disp=False)

        # natural frequency analysis
        model.runNFA(modes=10)
        freq = model.getFrequency(modes=10)
        for freqs in freq:
            print(freqs)

        """
        # get mode shapes
        U = defaultdict(list)
        for mode in range(1,modes+1):
            print('Getting shapes for mode: {}'.format(mode))
            U[mode] = model.getModeShapes(mode=mode)

        return freq
        """

    finally:
        model.close()
        #core.stop()
        print('closed model')

def writeResults(coords,freq,U):
    # write shapes to file
    for ent in U:
        with open('route19-shapes-mode-{}.csv'.format(ent),'w',newline='') as f:
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

def testnames(path,name,scratch):
    time.sleep(1)
    print(path)
    print(name)
    print(scratch)

def main():
    path = r'C:\Users\John\repos\brp\0705151\Models\Apriori'
    name = r'LiftSpan_apriori.st7'
    scratch = r'C:\Temp'

    steps = 100

    # start 5 worker process
    with Pool(processes=steps) as pool:
        # run each model
        pool.starmap(testnames,zip(repeat(path,steps),
                                   repeat(name,steps),
                                   repeat(scratch,steps)))
if __name__ == '__main__':
    # initialize api
    #core.start()
    main()
    #timeit.timeit('main()',number=1)

    # release api
    #core.stop()
