import numpy as np
import wave

def enframe(y, frameSize, overlap):
	if len(y.shape) == 2:
		y = np.mean(y, axis=1)
		y.shape = (-1, 1)

	step = frameSize - overlap
	frameCount = int(np.floor((len(y)-overlap)/step))
	out = np.matrix(np.zeros((frameSize, frameCount), dtype=np.float64))
	for i in range(0, frameCount):
		startIndex = i*step
		out[:, i] = y[startIndex:(startIndex+frameSize), 0]
	return out

def audioread(fileName):
	#fs, au = scipy.io.wavfile.read(fileName)
	audioFile = wave.open(fileName, 'rb')
	# get file information and read sample data as string bytes
	nChannels, bytePerSample, fs, nFrames = audioFile.getparams()[:4]
	strData = audioFile.readframes(nFrames)
	audioFile.close()
	if bytePerSample > 4:
		raise ValueError('Bit per sample can not be greater than 4.')
	elif bytePerSample == 4:
		au = np.matrix(np.fromstring(strData, dtype=np.int32)/(2**(bytePerSample*8-1)), dtype=np.float64).reshape(-1, nChannels)
	elif bytePerSample == 3:
		au = np.matrix(np.array([int.from_bytes(strData[i:i+bytePerSample], byteorder='little', signed=True) for i in range(0, len(strData), bitPerSample)], dtype=np.float64)/(2**(bitPerSample*8-1))).reshape(-1, nChannels)
	elif bytePerSample == 2:
		au = np.matrix(np.fromstring(strData, dtype=np.int16)/(2**(bytePerSample*8-1)), dtype=np.float64).reshape(-1, nChannels)
	elif bytePerSample == 1:
		au = np.matrix((np.array(np.fromstring(strData, dtype=np.uint8), dtype=np.float64)-128)/(2**(bitPerSample*8-1))).reshape(-1, nChannels)
	return (fs, au)

def audiowrite(fileName, au, fs, **kwargs):
	if len(kwargs) == 0:
		bitPerSample = 16
	else:
		for i in kwargs:
			if i == 'bitPerSample':
				bitPerSample = kwargs[i]
	if (bitPerSample % 8 != 0) or (bitPerSample > 32):
		raise ValueError('Bit per sample should be 8, 16, 24 or 32.')
	au = au*(2**(bitPerSample-1))
	if bitPerSample == 8:
		au = au + 128
		au = au.astype(np.uint8)
	elif bitPerSample == 16:
		au = au.astype(np.int16)
	elif bitPerSample == 24:
		pass
	elif bitPerSample == 32:
		au = au.astype(np.int32)
	audioFile = wave.open(fileName, 'wb')
	audioFile.setnchannels(au.shape[1])
	audioFile.setsampwidth(int(bitPerSample/8))
	audioFile.setframerate(fs)
	audioFile.writeframes(au.tostring())
	audioFile.close()

def main():
	fs, au = audioread('testAudio/mono.wav')
	audiowrite('test.wav', au, fs)
	audiowrite('test8.wav', au, fs, bitPerSample=8)
	audiowrite('test16.wav', au, fs, bitPerSample=16)
	audiowrite('test32.wav', au, fs, bitPerSample=32)


if __name__ == '__main__':
	main()