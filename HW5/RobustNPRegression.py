from kernels.Kernels import Kernels
from parameters.RobustNPRegressionParameters import RobustNPRegressionParameters
import random
import math

class RobustNPRegression:
    MIN_K = 5
    MAX_K = 20
    STEP_K = 1

    def __init__(self, data):
        self.data = data

    def lowless(self, data, parameters):
        length = len(data)
        gammas = [1.0 for _ in range(length)]
        prevGammas = []

        epsilon = 10 ** (-5)

        def stop(a, b):
            for i in range(len(a)):
                if abs(a[i] - b[i]) > epsilon:
                    return False
            return True

        while True:
            prevGammas = list(gammas)
            ass = [0 for _ in range(length)]
            for i in range(length):
                pi = data[i]
                distances = []
                for j in range(length):
                    if j != i:
                        distances.append(abs(pi[0] - data[j][0]))
                distances = sorted(distances)
                h = distances[parameters.k + 1]
                sum1 = 0.0
                sum2 = 0.0
                for j in range(length):
                    if j != i:
                        pj = data[j]
                        sum1 += pj[1] * gammas[j] * parameters.kernel(abs(pj[0] - pi[0]) / h)
                        sum2 += gammas[j] * parameters.kernel(abs(pj[0] - pi[0]) / h)
                ass[i] = abs(pi[1] - (sum1 / sum2))
            var = list(ass)
            med = 0
            if length % 2 == 0:
                med = (var[(length - 1) // 2] + var[(length - 1) // 2 + 1]) / 2.0
            else:
                med = var[(length - 1) // 2]
            var = sorted(var)
            for i in range(length):
                gammas[i] = Kernels(3).apply(abs(ass[i]) / (6 * med))
            if not stop(gammas, prevGammas):
                break
        return gammas

    def evaluate(self, point, parameters):
        sum1 = 0.0
        sum2 = 0.0
        distances = []
        for train in parameters.train:
            distances.append(abs(point[0]- train[0]))
        distances = sorted(distances)
        h = distances[parameters.k + 1]

        for i in range(len(parameters.train)):
            train = parameters.train[i]
            sum1 += train[1] * parameters.gamma[i] * parameters.kernel(abs(point[0] - train[0]) / h)
            sum2 += parameters.gamma[i] * parameters.kernel(abs(point[0] - train[0]) / h)
        return [point[0], float('inf') if sum2 == 0 else sum1 / sum2]

    def learn(self, data):
        parameters = RobustNPRegressionParameters(None, None, [], 0, [], float('inf'))
        random.shuffle(data)

        for kernel, kname in Kernels.get_kernels(Kernels):
            for k in range(self.MIN_K, self.MAX_K, self.STEP_K):
                mse = 0.0
                gammas = self.lowless(data, RobustNPRegressionParameters(kernel, kname, data, k, None, mse))
                for i in range(len(data)):
                    xi = data[i]
                    train = list(data)
                    train = train[:i] + train[i + 1:]
                    a = self.evaluate(xi, RobustNPRegressionParameters(kernel, kname, train, k, gammas, mse))
                    mse += math.pow(a[1] - xi[1], 2.0)
                mse /= len(data)
                if mse < parameters.mse:
                    parameters = RobustNPRegressionParameters(kernel, kname, data, k, gammas, mse)
        return parameters
