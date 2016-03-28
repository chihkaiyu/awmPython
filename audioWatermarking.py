import numpy as np
import util

class AudioWatermarkingMCLT():
	pass

	def __init__(self):
		pass

	def awmEmbed(self, au, awmOpt):
		# set variables
		M = int(awmOpt.frameSize / 2)
		C = AudioWatermarkingMCLT.co(M)
		S = AudioWatermarkingMCLT.si(M)
		W = AudioWatermarkingMCLT.Wa(M)
		C1 = C[:, 0:M]
		C2 = C[:, M:2*M]
		S1 = S[:, 0:M]
		S2 = S[:, M:2*M]
		W1 = W[0:M, 0:M]
		W2 = W[M:2*M, M:2*M]
		A_1 = C1 * W1 * W2 * S2.transpose()
		A1 = C2 * W2 * W1 * S1.transpose()
		B_1 = S1 * W1 * W2 * C2.transpose()
		B1 = S2 * W2 * W1 * C1.transpose()
		syncSeq = awmOpt.syncSeq.reshape(int((awmOpt.syncFreqBand[1]-awmOpt.syncFreqBand[0])/2+1) , -1)
		dataSeq = AudioWatermarkingMCLT.string2binary(awmOpt.data)
		bitPerFrame = int((awmOpt.dataFreqBand[1]-awmOpt.dataFreqBand[0]+1) / awmOpt.spreadLen)
		syncFrameSize = int(np.size(syncSeq) / ((awmOpt.syncFreqBand[1]-awmOpt.syncFreqBand[0])/2+1)*2)
		dataFrameSize =  int(np.ceil(np.size(dataSeq)/bitPerFrame))
		blockSize = syncFrameSize + dataFrameSize
		frameMat = util.enframe(au, awmOpt.frameSize, awmOpt.overlap)
		# data matrix
		if (np.size(dataSeq) % bitPerFrame) != 0:
			zeroToBePadded = np.zeros((1, dataFrameSize*bitPerFrame-np.size(dataSeq)), dtype=int)
			remainPart = np.size(zeroToBePadded)
			dataSeq = np.concatenate((dataSeq, zeroToBePadded), 1)
		data = np.kron(np.ones((awmOpt.spreadLen, 1)), dataSeq).reshape(awmOpt.dataFreqBand[1]-awmOpt.dataFreqBand[0]+1, -1)

		# fast MCLT
		fmcltk = np.array(range(0, M+1), dtype=np.float64)
		fmcltc = AudioWatermarkingMCLT.compExpo(8, 2*fmcltk+1) * AudioWatermarkingMCLT.compExpo(4*M, fmcltk)
		X = AudioWatermarkingMCLT.fmclt2(frameMat, fmcltc)

		# data Embed
		xBar = X
		Xc = X.real
		Xs = -X.imag
		for b in range(0, int(np.floor(X.shape[1]/blockSize))*blockSize, blockSize):
			# synchronization
			# i is for frame index
			# k is for frequency index
			i = range(b+1, b+syncFrameSize-1, 2)
			k = range(awmOpt.syncFreqBand[0], awmOpt.syncFreqBand[1], 2)
			xBarCSub = A_1[np.ix_(k, range(0, A_1.shape[1]))]*Xs[np.ix_(range(Xs.shape[0]), i-1)] + 0.5*Xs[np.ix_(k-1, i)] - 0.5*Xs[np.ix_(k+1, i)] + A1[np.ix_(k, range(0, A1.shape[1]))]*Xs[np.ix_(range(0, Xs.shape[0]), i+1)]
			XBarC = np.absolute(X[np.ix_(k, i)]) 



	#def awmExtract(self):
	
	@staticmethod
	def compExpo(M, r):
		return np.exp(-1j*2*np.pi*r/M)

	@staticmethod
	def fmclt(x):
		# MCLT of a single vector
		M = len(x)/2
		U = np.float64(np.sqrt(1/(2*M))) * np.fft.fft(x)
		k = np.array(range(0, M+1), dtype=np.float64)
		c = AudioWatermarkingMCLT.compExpo(8, 2*k+1) * AudioWatermarkingMCLT.compExpo(4*M, k)
		V = c * U[0:M+1]
		X = 1j * V[0:M] + V[1:M+1]
		return X

	@staticmethod
	def fmclt2(frameMat, c):
		# MCLT of a frame matrix
		M = frameMat.shape[0]/2
		X = np.zeros((M, frameMat.shape[1]), dtype=np.complex_)
		for i in range(frameMat.shape[1]):
			U = np.float64(np.sqrt(1/(2*M))) * np.fft.fft(frameMat[:, i])
			V = c * U[0:M+1]
			X[:, i] = 1j * V[0:M] + V[1:M+1]
		return X

	@staticmethod
	def fimclt(X):
		M = len(X)
		Y = np.zeros((2*M,), dtype=np.complex_)
		k = np.array(range(1, M), dtype=np.float64)
		c = AudioWatermarkingMCLT.compExpo(8, 2*k+1) * AudioWatermarkingMCLT.compExpo(4*M, k)
		Y[1:M] = (1/4) * np.conj(c) * (X[0:M-1] - 1j * X[1:M])
		Y[0] = np.sqrt(1/8) * (X[0].real + X[0].imag)
		Y[M] = -np.sqrt(1/8) * (X[M-1].real + X[M-1].imag)
		Y[M+1:2*M] = np.conj(Y[range(M-1, 0, -1)])
		y = np.fft.ifft(np.sqrt(2*M) * Y).real
		return y

	@staticmethod
	def string2binary(message):
		ascii = [bin(ord(i))[2:].zfill(8) for i in message]
		code = np.array(list(''.join(ascii)), dtype=int)
		pos = (code==0).nonzero()
		code[pos] = -1
		return code

	@staticmethod
	def cipher2plain(cipher):
		pos = (cipher == -1).nonzero()
		cipher[pos] = 0
		cipher = ''.join(str(i) for i in cipher)
		byte = [cipher[i:i+8] for i in range(0, len(cipher), 8)]
		plain = ''.join(chr(int(i, 2)) for i in byte)
		return plain

	@staticmethod
	def co(M):
		C = np.array([[np.sqrt(2/M)*np.cos((j+((M+1)/2))*(i+0.5)*np.pi/M) for j in range(0, 2*M)] for i in range(0, M)], dtype=np.float64)
		return C

	@staticmethod
	def si(M):
		S = np.array([[np.sqrt(2/M)*np.sin((j+((M+1)/2))*(i+0.5)*np.pi/M) for j in range(0, 2*M)] for i in range(0, M)], dtype=np.float64)
		return S

	@staticmethod
	def Wa(M):
		W = np.diag(np.array([-np.sin((i+0.5)*np.pi/(2*M)) for i in range(0, 2*M)], dtype=np.float64))
		return W

def main():
	from awmOpt import AwmOptSet
	import util
	fs, au = util.audioread('./testAudio/classical.wav')
	awmOpt = AwmOptSet()
	awmOpt.display()
	awm = AudioWatermarkingMCLT()
	awm.awmEmbed(au, awmOpt)

if __name__ == '__main__':
	main()