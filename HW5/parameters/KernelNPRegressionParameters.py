class KernelNPRegressionParameters:
    def __init__(self, h, kernel, kname, train, isHConstant, k, mse):
        self.h = h
        self.kernel = kernel
        self.kname = kname
        self.train = train
        self.isHConstant = isHConstant
        self.k = k
        self.mse = mse

    def __str__(self):
        return 'train = %s\nh = %s, kernel = %s, h - %s, k = %s, mse = %s' % (str(self.train), str(self.h), str(self.kname), 'constant' if self.isHConstant else 'not constant', str(self.k), str(self.mse))
