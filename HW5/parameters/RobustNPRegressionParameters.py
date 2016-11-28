class RobustNPRegressionParameters:
    def __init__(self, kernel, kname, train, k, gamma, mse):
        self.kernel = kernel
        self.kname = kname
        self.train = train
        self.k = k
        self.gamma = gamma
        self.mse = mse

    def __str__(self):
        return 'train = %s\nkernel = %s, k = %s, mse = %s\ngamma = %s' % (
        str(self.train), str(self.kname), str(self.k), str(self.mse), str(self.gamma))
