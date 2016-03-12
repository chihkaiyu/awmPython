import scipy.io.wavfile
import numpy as np
from awmOptSet import AwmOpt

class AWM:
    pass

    def __init__(self, fileName, awmOpt):
        self.awmOpt = awmOpt
        # audio read
        if type(fileName) == str:
            self.fs, self.au = scipy.io.wavfile.read(fileName)
            # convert to float64 and normalize between -1 and 1
            if self.au.dtype == 'int8':
                self.au = self.au.astype(np.double) / (2**7)
            elif self.au.dtype == 'int16':
                self.au = self.au.astype(np.double) / (2**15)
            elif self.au.dtype == 'int24':
                self.au = self.au.astype(np.double) / (2**23)
        else:
            self.au = fileName

    def setAwmOpt(self, key, value):
        self.awmOpt.setOpt(key, value)

    def displayAwmOpt(self):
        self.awmOpt.displayOpt()
    #def awmEmbed():

    #def awmExtract():

    #def __fmclt():
    
def main():
    awmOpt = AwmOpt()
    au = AWM('/home/kai/Documents/originalAudio/rock.wav', awmOpt)
    au.awmOpt.Opt()
    au.setAwmOpt('data', 'chutchut')
    au.setAwmOpt('syncFreqBand', [233, 288])
    au.displayAwmOpt()
    #print(au.au[88200:88220])

if __name__ == '__main__':
    main()