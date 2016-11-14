import math

class Kernels:
    kernels = [
        lambda u: 0.5 * (1 if abs(u) <= 1 else 0),
        lambda u: 3.0 / 4 * (1 - u**2) * (1 if abs(u) < 1 else 0),
        lambda u: 15.0 / 16 * (1 - u**2)**2 * (1 if abs(u) < 1 else 0),
        lambda u: 35.0 / 32 * (1 - u**2)**3 * (1 if abs(u) < 1 else 0),
        lambda u: 1.0 / math.sqrt(2 * math.pi) * math.exp(-0.5 * u**2)
    ]

    def __init__(self, id):
        self.kernel = self.kernels[id]

    @staticmethod
    def get(self, u):
        return self.kernel(u)

    @staticmethod
    def get_kernels(self):
        return self.kernels
