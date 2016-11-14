import math

class Distances:
    distances = [
        lambda x, y: sum(abs(x[i] - y[i]) for i in range(len(x))),
        lambda x, y: math.sqrt(sum((x[i] - y[i]) ** 2 for i in range(len(x)))),
        lambda x, y: max(abs(x[i] - y[i]) for i in range(len(x)))
    ]

    def __init__(self, id):
        self.distance = self.distances[id]

    @staticmethod
    def get(self, x, y):
        return self.distance(x, y)

    @staticmethod
    def get_distances(self):
        return self.distances
