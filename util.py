import numpy as np
import scipy.io.wavfile

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

def audioread(fileName):
	fs, au = scipy.io.wavfile.read(fileName)
	# conver to float64 and normalize between -1 and 1
	if au.dtype == 'int8':
		au = au.astype(np.float64) / (2**7)
	elif au.dtype == 'int16':
		au = au.astype(np.float64) / (2**15)
	elif au.dtype == 'int24':
		au = au.astype(np.float64) / (2**23)
	elif au.dtype == 'int32':
		au = au.astype(np.float64) / (2**31)
	elif au.dtype == 'int64':
		au = au.astype(np.float64) / (2**63)
	return (fs, au)
