from classifiers.knn.parameters.Parameters import Parameters
from classifiers.parameters.Distances import Distances
from classifiers.knn.parameters.Transformations import Transformations
from classifiers.knn.parameters.Kernels import Kernels
from classifiers.dividers.Divider import Divider


class KNN:
    MIN_K = 5
    MAX_K = 15
    CV_SIZE = 5

    def __init__(self, data):
        self.data = data

    def evaluate(self, _train, _test, parameters):
        answer = []
        train = parameters.transformation(_train)
        test = parameters.transformation(_test)

        for t in test:
            distances = []
            for tr in train:
                distances.append([parameters.distance(t[:-1], tr[:-1]), tr[-1]])
            distances = sorted(distances)
            biggest_distance = distances[parameters.k][0]
            voices = [0, 0]
            for i in range(parameters.k):
                point = distances[i]
                importance = parameters.kernel(point[0] / biggest_distance)
                voices[point[1]] += importance
            clazz = 0 if voices[0] > voices[1] else 1
            answer.append([t[0], t[1], clazz])
        return answer

    def run(self, size, parameters):
        divider = Divider(self.data, size)
        accuracy = 0.0
        for div in divider.divided:
            answer = self.evaluate(div[0], div[1], parameters)
            accuracy += parameters.measure.get(div[1], answer)
        return accuracy / len(divider.divided)

    def learn(self, data, measure):
        knn_params = Parameters()
        for k in range(self.MIN_K, self.MAX_K + 1):
            for distance in Distances.get_distances(Distances):
                for kernel in Kernels.get_kernels(Kernels):
                    for transformation in Transformations.get_transformations(Transformations):
                        result = KNN(data).run(self.CV_SIZE, Parameters(distance, kernel, transformation, k, 0, measure))
                        if knn_params.accuracy < result:
                            knn_params = Parameters(distance, kernel, transformation, k, result, measure)

        knn_params.measure = measure
        return knn_params
