class Metrics:
    def __init__(self):
        pass

    @staticmethod
    def minkowski_metric(p):
        return lambda x, y: sum(((abs(x[i] - y[i]) ** p) ** (1. / p)) for i in range(len(x)))

    @staticmethod
    def get_all_metrics(self):
        return [(self.minkowski_metric(1), 'Manhattan metric'),
                (self.minkowski_metric(2), 'Euclid metric')]