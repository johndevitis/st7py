"""
this is an example class
"""


class John(object):

    cnt = 0
    chk = True

    def __init__(self):
        # increment global class counter
        John.cnt += 1

        # assign unique global count to instance
        self.cnt = John.cnt

    def identify(self):
        print(self.__name__)

    def bendover(self):
        atts = vars(self)
        print('\n'.join('%s: %s' % item for item in atts).items())

def bar(base):
    if base.cnt % 2 == 0:
        base.chk = False
    else:
        base.chk = True

def main():
    # test auto incrementing counter property
    for i in range(10):
        john = John()
        print(john.cnt)
        bar(john)
        print(john.chk)

if __name__ == '__main__':
    main()
