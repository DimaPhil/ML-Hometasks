from classifiers.knn.parameters.Kernels import Kernels
from classifiers.knn.parameters.Transformations import Transformations
from classifiers.parameters.Distances import Distances
from classifiers.parameters.Measures import Measures


class Parameters:
    def __init__(self, distance=Distances(1), kernel=Kernels(0), transformation=Transformations(0), k=0, accuracy=0,
                 measure=Measures(0)):
        self.distance = distance
        self.kernel = kernel
        self.transformation = transformation
        self.k = k
        self.accuracy = accuracy
        self.measure = measure
