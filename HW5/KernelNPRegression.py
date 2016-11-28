from parameters.KernelNPRegressionParameters import KernelNPRegressionParameters
from kernels.Kernels import Kernels
import random
import math


class KernelNPRegression:
    MIN_H = 10 ** (-9)
    MAX_H = 10 ** 9
    STEP_H = 10

    MIN_K = 5
    MAX_K = 20
    STEP_K = 1

    def __init__(self, data):
        self.data = data

    def evaluate(self, point, parameters):
        sum1 = 0
        sum2 = 0
        h = parameters.h
        if not parameters.isHConstant:
            distances = []
            for train in parameters.train:
                distances.append(abs(point[0] - train[0]))
            distances = sorted(distances)
            h = distances[parameters.k + 1]
        for train in parameters.train:
            sum1 += train[1] * parameters.kernel(abs(point[0] - train[0]) / h)
            sum2 += parameters.kernel(abs(point[0] - train[0]) / h)
        return [point[0], float('inf') if sum2 == 0 else sum1 / sum2]

    def learn(self, data):
        parameters = KernelNPRegressionParameters(self.MIN_H, Kernels(4), 'GAUSSIAN', [], True, self.MIN_H, float('inf'))
        random.shuffle(data)

        for kernel, kname in Kernels.get_kernels(Kernels):
            h = self.MIN_H
            while h <= self.MAX_H:
                mse = 0.0
                for i in range(len(data)):
                    xi = data[i]
                    train = list(data)
                    train = train[:i] + train[i + 1:]
                    a = self.evaluate(xi, KernelNPRegressionParameters(h, kernel, kname, train, True, self.MIN_K, 0.0))
                    mse += math.pow(a[1] - xi[1], 2.0)
                mse /= len(data)
                if mse < parameters.mse:
                    parameters = KernelNPRegressionParameters(h, kernel, kname, data, True, self.MIN_K, mse)
                h *= self.STEP_H
            for k in range(self.MIN_K, self.MAX_K + 1, self.STEP_K):
                mse = 0.0
                for i in range(len(data)):
                    xi = data[i]
                    train = list(data)
                    train = train[:i] + train[i + 1:]
                    a = self.evaluate(xi, KernelNPRegressionParameters(self.MIN_H, kernel, kname, train, False, k, 0.0))
                    mse += math.pow(a[1] - xi[1], 2)
                mse /= len(data)
                if mse < parameters.mse:
                    parameters = KernelNPRegressionParameters(self.MIN_H, kernel, kname, data, False, k, mse)
        return parameters
