import scipy.io.wavfile
import numpy as np
from awmOptSet import AwmOpt
import util

class AWM:
    pass

    def __init__(self, fileName, awmOpt):
        self.awmOpt = awmOpt
        # audio read
        if type(fileName) == str:
            self.fs, self.au = scipy.io.wavfile.read(fileName)
            # convert to float64 and normalize between -1 and 1
            if self.au.dtype == 'int8':
                self.au = self.au.astype(np.float64) / (2**7)
            elif self.au.dtype == 'int16':
                self.au = self.au.astype(np.float64) / (2**15)
            elif self.au.dtype == 'int24':
                self.au = self.au.astype(np.float64) / (2**23)
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
    awm = AWM('./originalAudio/classical.wav', AwmOpt())
    awm.displayAwmOpt()
    frame = util.enframe(awm.au, awm.awmOpt.frameSize, awm.awmOpt.overlap)
    print(frame.shape)

if __name__ == '__main__':
    main()