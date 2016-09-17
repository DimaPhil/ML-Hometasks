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
    def get_all_transformations(self):
        return [(self.automorphism(), 'Automorphism, no changes'),
                (self.increasing_dimension_transform(), '[x, y] -> [x, y, x * y, x^2, y^2]')]