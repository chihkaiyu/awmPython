import scipy.io.wavfile
import numpy as np

class AWM:
    pass

    def __init__(self, fileName):
        # awmOpt
        self.frameSize = 1024
        self.syncFreqBand = [149, 185]
        self.dataFreqBand = [149, 184]
        self.spreadLen = 36
        self.overlap = 512
        self.data = 'Mirlab'
        self.syncSeq = np.array([[1, 1, -1, 1, 1, -1, -1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, 1, 1], [1, 1, -1, 1, 1, 1, 1, 1, -1, 1, -1, 1, -1, -1, -1, -1, 1, 1, -1], [1, -1, -1, -1, 1, 1, -1, -1, -1, 1, 1, 1, -1, 1, 1, -1, -1, -1, 1], [-1, 1, -1, 1, -1, 1, 1, 1, 1, 1, -1, -1, -1, 1, -1, 1, -1, 1, -1], [-1, -1, 1, -1, -1, 1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, 1, 1, 1], [-1, 1, -1, -1, -1, -1, 1, -1, 1, -1, 1, -1, 1, 1, 1, -1, -1, -1, 1]])
        self.method = 'mclt'

        # audio read
        if type(fileName) == str:
            self.fs, self.au = scipy.io.wavfile.read(fileName)
            # convert to float64 and normalize between -1 and 1
            if self.au.dtype == 'int16':
                self.au = self.au.astype(np.double) / (2**15)
            elif self.au.dtype == 'int24':
                self.au = self.au.astype(np.double) / (2**23)
        else:
            self.au = fileName

    def Opt(self):
        print('Frame size: {0}'.format(self.frameSize))
        print('Overlap: {0}'.format(self.overlap))
        print('Sample rate: {0}'.format(self.fs))
        print('Sync. target band: {0}'.format(self.syncFreqBand))
        print('Data target band: {0}'.format(self.dataFreqBand))
        print('Spreading length: {0}'.format(self.spreadLen))
        print('Data: {0}'.format(self.data))
        print('Method: {0}'.format(self.method))

    def setOpt(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            print('Undefined option: %s' % (key))

    #def awmEmbed():

    #def awmExtract():

    #def __fmclt():
    
def main():
    au = AWM('/home/kai/Documents/originalAudio/rock.wav')
    au.Opt()
    au.setOpt('data', 'chutchut')
    au.setOpt('syncFreqBand', [233, 288])
    au.Opt()
    #print(au.au[88200:88220])

if __name__ == '__main__':
    main()