"""
solvers/nfa
=======

jdv 11062016
"""

settings = {"enableNSMcase": True,
            "modeParticipation": True,
            }

def run():
    """perform a natural frequency analysis"""
    print('Natural Frequency Analysis:')

    # show current settings
    print('\tCurrent settings:')
    for k, v in settings.items():
        print('\t\t{:20}\t{}'.format(k, v))

def updateSettings(**kwargs):
    print('Updating Settings...')

def runNFA(self, nmodes=5):
    # set up result file name
    resName = os.path.splitext(self._fullname)[0] + '.nfa'.encode()
    # set number of modes to calculate
    chkErr(St7SetNFANumModes(self.uID, nmodes))
    # run solver
    chkErr(St7RunSolver(self.uID, stNaturalFrequencySolver, smBackgroundRun, btTrue))


if __name__ == '__main__':
    """run defaults if called directly"""
    run()