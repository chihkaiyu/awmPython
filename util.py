import numpy as np
import wave
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
	#fs, au = scipy.io.wavfile.read(fileName)
	audioFile = wave.open(fileName, 'rb')
	# get file information and read sample data as string bytes
	nChannels, bitPerSample, fs, nFrames = audioFile.getparams()[:4]
	strData = audioFile.readframes(nFrames)
	audioFile.close()
	if bitPerSample > 4:
		raise ValueError('Bit per sample can not be greater than 4.')
	elif bitPerSample == 4:
		au = np.matrix(np.fromstring(strData, dtype=np.int32)/(2**(bitPerSample*8-1)), dtype=np.float64).reshape(-1, nChannels)
	elif bitPerSample == 3:
		au = np.matrix(np.array([int.from_bytes(strData[i:i+bitPerSample], byteorder='little', signed=True) for i in range(0, len(strData), bitPerSample)], dtype=np.float64)/(2**(bitPerSample*8-1))).reshape(-1, nChannels)
	elif bitPerSample == 2:
		au = np.matrix(np.fromstring(strData, dtype=np.int16)/(2**(bitPerSample*8-1)), dtype=np.float64).reshape(-1, nChannels)
	elif bitPerSample == 1:
		au = np.matrix((np.array(np.fromstring(strData, dtype=np.uint8), dtype=np.float64)-128)/(2**(bitPerSample*8-1))).reshape(-1, nChannels)

	'''
	if au.dtype == 'uint8':
		au = np.matrix(au.astype(np.float64) / (2**7)).reshape(au.shape[0], -1)
	elif au.dtype == 'int16':
		au = np.matrix(au.astype(np.float64) / (2**15)).reshape(au.shape[0], -1)
	else:
		au = np.matrix(au.astype(np.float64)).reshape(au.shape[0], -1)
	'''
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
		print(au[44100])
		print('==========================')


if __name__ == '__main__':
	main()