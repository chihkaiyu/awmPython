import numpy as np
from awmOptSet import AwmOpt
import util
import awmUtil

class AWM:
    pass
    '''
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
    '''
    #def awmEmbed():

    #def awmExtract():

    #def __fmclt():
    
def main():
    #awm = AWM('./testAudio/classical.wav', AwmOpt())
    awmOpt = AwmOpt()
    awmOpt.display()
    fs, au = util.audioread('./testAudio/classical.wav')
    frame = util.enframe(au, awmOpt.frameSize, awmOpt.overlap)
    M=512
    fmcltk = np.array(range(0, M+1), dtype=np.float64)
    fmcltc = awmUtil.compExpo(8, 2*fmcltk+1) * awmUtil.compExpo(4*M, fmcltk)
    X = awmUtil.fmclt2(frame, fmcltc)
    print(X.shape)
    print(X.dtype)
    yBar = np.zeros((1024, X.shape[1]), dtype=np.float64)
    for i in range(X.shape[1]):
        yBar[:, i] = awmUtil.fimclt(X[:, i])
    print(yBar.shape)
    print(yBar.dtype)

if __name__ == '__main__':
    main()