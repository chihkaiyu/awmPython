class AwmOpt:
	pass

	def __init__(self):
		# awmOpt
		self.frameSize = 1024
        self.syncFreqBand = [149, 185]
        self.dataFreqBand = [149, 184]
        self.spreadLen = 36
        self.overlap = 512
        self.data = 'Mirlab'
        self.syncSeq = np.array([[1, 1, -1, 1, 1, -1, -1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, 1, 1], [1, 1, -1, 1, 1, 1, 1, 1, -1, 1, -1, 1, -1, -1, -1, -1, 1, 1, -1], [1, -1, -1, -1, 1, 1, -1, -1, -1, 1, 1, 1, -1, 1, 1, -1, -1, -1, 1], [-1, 1, -1, 1, -1, 1, 1, 1, 1, 1, -1, -1, -1, 1, -1, 1, -1, 1, -1], [-1, -1, 1, -1, -1, 1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, 1, 1, 1], [-1, 1, -1, -1, -1, -1, 1, -1, 1, -1, 1, -1, 1, 1, 1, -1, -1, -1, 1]])
        self.method = 'mclt'

    def setOpt(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            print('Undefined option: %s' % (key))

    def displayOpt(self):
	    print('Frame size: {0}'.format(self.frameSize))
	    print('Overlap: {0}'.format(self.overlap))
	    print('Sample rate: {0}'.format(self.fs))
	    print('Sync. target band: {0}'.format(self.syncFreqBand))
	    print('Data target band: {0}'.format(self.dataFreqBand))
	    print('Spreading length: {0}'.format(self.spreadLen))
	    print('Data: {0}'.format(self.data))
	    print('Method: {0}'.format(self.method))