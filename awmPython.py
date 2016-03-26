import numpy as np
from awmOptSet import AwmOpt
import util
from AWM import AudioWatermarking as awm

    
def main():
    #awm = AWM('./testAudio/classical.wav', AwmOpt())
    awmOpt = AwmOpt()
    awmOpt.display()
    fs, au = util.audioread('./testAudio/classical.wav')
    frame = util.enframe(au, awmOpt.frameSize, awmOpt.overlap)
    M=512
    fmcltk = np.array(range(0, M+1), dtype=np.float64)
    fmcltc = awm.compExpo(8, 2*fmcltk+1) * awm.compExpo(4*M, fmcltk)
    X = awm.fmclt2(frame, fmcltc)
    print(X.shape)
    print(X.dtype)
    yBar = np.zeros((1024, X.shape[1]), dtype=np.float64)
    for i in range(X.shape[1]):
        yBar[:, i] = awm.fimclt(X[:, i])
    print(yBar.shape)
    print(yBar.dtype)

if __name__ == '__main__':
    main()