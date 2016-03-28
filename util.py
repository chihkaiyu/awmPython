import numpy as np
import scipy.io.wavfile

def enframe(y, frameSize, overlap):
	if len(y.shape) == 2:
		y = np.mean(y, axis=1)
		y.shape = (-1, 1)

	step = frameSize - overlap
	frameCount = int(np.floor((len(y)-overlap)/step))
	out = np.matrix(np.zeros((frameSize, frameCount), dtype=np.float64))
	for i in range(frameCount):
		startIndex = i*step+1
		out[:, i] = y[startIndex:(startIndex+frameSize), 0]
	return out

def audioread(fileName):
	fs, au = scipy.io.wavfile.read(fileName)
	# conver to float64 and normalize between -1 and 1
	if au.dtype == 'uint8':
		au = np.matrix(au.astype(np.float64) / (2**7)).reshape(au.shape[0], -1)
	elif au.dtype == 'int16':
		au = np.matrix(au.astype(np.float64) / (2**15)).reshape(au.shape[0], -1)
	else:
		au = np.matrix(au.astype(np.float64)).reshape(au.shape[0], -1)
	return (fs, au)

def main():
	import os
	fileList = os.listdir('./testAudio/')
	for i in fileList:
		fs, au = audioread(os.path.join(os.getcwd(), 'testAudio', i))
		print('==========================')
		print(i)
		print(au.dtype)
		print(au.shape)
		print('==========================')


if __name__ == '__main__':
	main()