import numpy as np

class AudioWatermarking():
	pass

	def __init__(self):
		pass

	def awmEmbed(self, au, awmOpt):
		# set variables
		M = awmOpt.frameSize / 2
		C = AudioWatermarking.co(M)
		S = AudioWatermarking.si(M)
		W = AudioWatermarking.Wa(M)
		C1 = C[:, 0:M]
		C2 = C[:, M:2*M]
		S1 = S[:, 0:M]
		S2 = S[:, M:2*M]
		W1 = W[1:M, 1:M]
		W2 = W[M:2*M, M:2*M]
		A_1 = C1 * W1 * W2 * S2.transpose()
		A1 = C2 * W2 * W1 * S1.transpose()
		B_1 = S1 * W1 * W2 * C2.transpose()
		B1 = S2 * W2 * W1 * C1.transpose()
		bitPerFrame = (awmOpt.dataFreqBand[1]-awmOpt.dataFreqBand[0]+1) / awmOpt.spreadLen
		syncSeq = awmOpt.syncSeq.reshape(int((awmOpt.syncFreqBand[1]-awmOpt.syncFreqBand[0])/2+1) , -1)
		dataSeq = AudioWatermarking.string2binary(awmOpt.data)



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
		c = AudioWatermarking.compExpo(8, 2*k+1) * AudioWatermarking.compExpo(4*M, k)
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
		c = AudioWatermarking.compExpo(8, 2*k+1) * AudioWatermarking.compExpo(4*M, k)
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