import numpy as np

class AwmOptSet:
    pass

    def __init__(self, method):
        if method == 'mclt':
            self.frameSize = 1024
            self.syncFreqBand = [149, 185]
            self.dataFreqBand = [149, 184]
            self.spreadLen = 36
            self.overlap = 512
            self.data = 'Mirlab'
            self.syncSeq = np.matrix([[1, 1, -1, 1, 1, -1, -1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, 1, 1], [1, 1, -1, 1, 1, 1, 1, 1, -1, 1, -1, 1, -1, -1, -1, -1, 1, 1, -1], [1, -1, -1, -1, 1, 1, -1, -1, -1, 1, 1, 1, -1, 1, 1, -1, -1, -1, 1], [-1, 1, -1, 1, -1, 1, 1, 1, 1, 1, -1, -1, -1, 1, -1, 1, -1, 1, -1], [-1, -1, 1, -1, -1, 1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, 1, 1, 1], [-1, 1, -1, -1, -1, -1, 1, -1, 1, -1, 1, -1, 1, 1, 1, -1, -1, -1, 1]])
            self.method = 'mclt'
        elif method == 'dct':
            pass
        else:
            print('Unknown method')

    def setOpt(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            print('Undefined option: %s' % (key))

    def display(self):
        print('==============================')
        print('Frame size: {0}'.format(self.frameSize))
        print('Overlap: {0}'.format(self.overlap))
        print('Sync. target band: {0}'.format(self.syncFreqBand))
        print('Data target band: {0}'.format(self.dataFreqBand))
        print('Spreading length: {0}'.format(self.spreadLen))
        print('Data: {0}'.format(self.data))
        print('Method: {0}'.format(self.method))
        print('==============================')