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
    def compressing_transform(xs, ys):
        minx = min(xs)
        maxx = max(xs)
        miny = min(ys)
        maxy = max(ys)
        nxs = []
        nys = []
        for x, y in zip(xs, ys):
            nxs.append((x - minx) / (maxx - minx))
            nys.append((y - miny) / (maxy - miny))
        return [nxs, nys]

    @staticmethod
    def get_all_transformations(self):
        return [(self.automorphism(), 'Automorphism, no changes'),
                (lambda xs, ys: self.compressing_transform(xs, ys), 'Compressing transform for [0, 1]x[0, 1]'),
                (self.increasing_dimension_transform(), '[x, y] -> [x, y, x * y, x^2, y^2]')]
