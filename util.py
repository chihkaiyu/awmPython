import numpy as np

def enframe(y, frameSize, overlap):
	if len(y.shape) == 2:
		y = np.mean(y, axis=1)
		y.shape = (-1, 1)

	step = frameSize - overlap
	frameCount = int(np.floor((len(y)-overlap)/step))
	out = np.zeros((frameSize, frameCount), dtype=np.float64)
	for i in range(frameCount):
		startIndex = i*step+1
		out[:, i] = y[startIndex:(startIndex+frameSize), 0]

	return out
def compExpo(M, r):
	return np.exp(-1j*2*np.pi*r/M)
	#w = np.zeros((len(r),), dtype=np.complex_)
	#for i in range(len(r)):
	#	w[i] = np.exp(-1j*2*math.pi*r[i]/M)
	#return w

def fmclt2(frameMat, c):
	M = frameMat.shape[0]/2
	X = np.zeros((M, frameMat.shape[1]), dtype=np.complex_)
	for i in range(frameMat.shape[1]):
		U = np.float64(np.sqrt(1/(2*M))) * np.fft.fft(frameMat[:, i])
		V = c * U[0:M+1]
		X[:, i] = 1j * V[0:M] + V[1:M+1]
	return X

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
