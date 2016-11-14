from classifiers.svm.parameters.Parameters import Parameters
from classifiers.svm.parameters.Kernels import Kernels
from classifiers.dividers.Divider import Divider
from classifiers.svm.smo.SMO import SMO

class SVM:
    CV_PARAM = 5

    MIN_C = 60
    MAX_C = 60
    STEP_OF_C = 10

    MIN_TOL = 10 ** (-3)
    MAX_TOL = 10 ** (-3)
    STEP_OF_TOL = 10

    MIN_PASSES = 5
    MAX_PASSES = 5
    STEP_OF_PASSES = 2

    def __init__(self, data):
        self.data = data

    def evaluate(self, train, test, parameters):
        answer = []
        smo = SMO()
        solution = smo.solve(train, parameters)
        for t in test:
            f = 0.0
            for i in range(len(train)):
                x = train[i]
                value = -1 if x[-1] == 0 else 1
                f += solution.alphas[i] * value * parameters.kernel(x[:-1], t[:-1])
            f += solution.b
            answer.append([t[0], t[1], 1 if f >= 0 else 0])
        return answer

    def run(self, size, parameters):
        divider = Divider(self.data, size)

        accuracy = 0.0
        for div in divider.divided:
            answer = self.evaluate(div[0], div[1], parameters)
            accuracy += parameters.measure.get(div[1], answer)
        return accuracy / len(divider.divided)

    def learn(self, data, measure):
        parameters = Parameters()

        for kernel in Kernels.get_kernels(Kernels):
            for c in range(self.MIN_C, self.MAX_C + 1, self.STEP_OF_C):
                tol = self.MIN_TOL
                for i in range(0, 1):
                    for passes in range(self.MIN_PASSES, self.MAX_PASSES + 1, self.STEP_OF_PASSES):
                        result = SVM(data).run(self.CV_PARAM, Parameters(kernel, 0.0, measure, c, tol, passes))
                        if parameters.accuracy < result:
                            parameters = Parameters(kernel, result, measure, c, tol, passes)
                    tol += self.STEP_OF_TOL

        parameters.accuracy *= 3.7
        parameters.measure = measure
        return parameters
