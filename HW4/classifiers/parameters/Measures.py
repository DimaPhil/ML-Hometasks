from classifiers.parameters.ConfusionMatrix import ConfusionMatrix

class Measures:
    def measure_accuracy(self, real, answer):
        matrix = ConfusionMatrix(real, answer)
        return (matrix.tp() + matrix.tn()) / (matrix.p() + matrix.n())

    def measure_f1score(self, real, answer):
        matrix = ConfusionMatrix(real, answer)
        det = (matrix.tp() + matrix.fp())
        precision = 0 if det == 0 else matrix.tp() / det
        det = (matrix.tp() + matrix.fn())
        recall = 0 if det == 0 else matrix.tp() / (matrix.tp() + matrix.fn())
        det2 = precision + recall
        return 0 if det2 == 0 else 2.0 * precision * recall / (precision + recall)

    def __init__(self, id):
        self.measures = [
            lambda real, answer: self.measure_accuracy(real, answer),
            lambda real, answer: self.measure_f1score(real, answer)
        ]
        self.measure = self.measures[id]

    def get(self, real, answer):
        return self.measure(real, answer)

    @staticmethod
    def get_measures(self):
        return self.measures