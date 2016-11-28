import math


class Kernels:
    kernels = [
        (lambda u: 0.5 * (1 if abs(u) <= 1.0 else 0), 'UNIFORM'),
        (lambda u: (1 - abs(u)) * (1 if abs(u) <= 1 else 0), 'TRIANGULAR'),
        (lambda u: (3.0 / 4 * (1 - u**2) * (1 if abs(u) <= 1 else 0)), 'EPANECHNIKOV'),
        (lambda u: (15.0 / 16 * (1 - u**2)**2 * (1 if abs(u) <= 1 else 0)), 'QUARTIC'),
        (lambda u: (1.0 / math.sqrt(2 * math.pi) * math.exp(-0.5 * u**2)), 'GAUSSIAN')
    ]

    def __init__(self, id):
        self.id = id
        self.kernel = self.kernels[id]

    def __str__(self):
        if self.id == 0:
            return "UNIFORM"
        elif self.id == 1:
            return "TRIANGULAR"
        elif self.id == 2:
            return "EPANECHNIKOV"
        elif self.id == 3:
            return "QUARTIC"
        else:
            return "GAUSSIAN"

    def apply(self, u):
        return self.kernel[0](u)

    @staticmethod
    def get_kernels(self):
        return self.kernels