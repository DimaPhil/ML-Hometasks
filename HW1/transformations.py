import math

class Transformations:
    def __init__(self):
        pass

    @staticmethod
    def automorphism():
        return lambda xs, ys: [xs, ys]

    @staticmethod
    def increasing_dimension_transform():
        return lambda xs, ys: list(zip(*tuple([x, y, x * y, x ** 2, y ** 2] for x, y in zip(xs, ys))))

    @staticmethod
    def square_transform():
        return lambda xs, ys: list(zip(*tuple([x ** 2, y ** 2] for x, y in zip(xs, ys))))

    @staticmethod
    def normalization(xs, ys):
        minx = min(xs)
        maxx = max(xs)
        miny = min(ys)
        maxy = max(ys)
        nxs = []
        nys = []
        for x, y in zip(xs, ys):
            nxs.append((x - minx) / (maxx - minx) * 2 - 1)
            nys.append((y - miny) / (maxy - miny) * 2 - 1)
        return [nxs, nys]

    @staticmethod
    def get_all_transformations(self):
        return [(self.automorphism(), 'Automorphism, no changes'),
                (self.square_transform(), '[x, y] -> [x^2, y^2]'),
                (self.increasing_dimension_transform(), '[x, y] -> [x, y, x * y, x^2, y^2]')]
