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