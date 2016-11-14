from classifiers.svm.parameters.Kernels import Kernels
from classifiers.parameters.Measures import Measures


class Parameters:
    def __init__(self, kernel=Kernels(0), accuracy=0, measure=Measures(1), c=0, tol=1e-3, maxPasses=5):
        self.kernel = kernel
        self.accuracy = accuracy
        self.measure = measure
        self.c = c
        self.tol = tol
        self.maxPasses = maxPasses