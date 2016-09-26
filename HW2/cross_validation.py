class CrossValidation:
    def __init__(self, elements, k):
        self.elements = elements
        self.k = k
        self.parts = len(elements) // k

    def iterations(self):
        return self.k

    def parts(self):
        return self.parts

    def divide(self, i):
        test = self.elements[i * self.parts:(i + 1) * self.parts]
        train = self.elements[:i * self.parts] + self.elements[(i + 1) * self.parts:]
        return test, train
