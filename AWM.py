import numpy as np

class AudioWatermarking():
	pass

	def __init__(self):
		pass

	def awmEmbed(self):

	def awmExtract(self):
	
	@staticmethod
	def compExpo(M, r):
		return np.exp(-1j*2*np.pi*r/M)

	@staticmethod
	def fmclt(x):
		# MCLT of a single vector
		M = len(x)/2
		U = np.float64(np.sqrt(1/(2*M))) * np.fft.fft(x)
		k = np.array(range(0, M+1), dtype=np.float64)
		c = compExpo(8, 2*k+1) * compExpo(4*M, k)
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
		c = compExpo(8, 2*k+1) * compExpo(4*M, k)
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