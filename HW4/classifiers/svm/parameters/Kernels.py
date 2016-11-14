import math
from classifiers.parameters.Distances import Distances

class Kernels:
    kernels = [
        lambda a, b: math.exp(-math.pow(Distances.get_distances(Distances)[1](a, b), 2.0) / 2.0)
    ]

    def __init__(self, id):
        self.kernel = self.kernels[id]

    @staticmethod
    def get(self, a, b):
        return self.kernel(a, b)

    @staticmethod
    def get_kernels(self):
        return self.kernels
