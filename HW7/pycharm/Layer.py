import numpy as np


class Layer:
    def __init__(self, shape, non_linearity, non_linearity_pr, learning_rate):
        self.x = 0
        self.r = 0
        self.o = 0
        self.W = np.random.normal(0, 0.02, shape)
        self.b = np.random.normal(0, 0.02, shape[1])
        self.non_linearity = non_linearity
        self.non_linearity_pr = non_linearity_pr
        self.learning_rate = learning_rate

    def forward(self, x):
        self.x = x
        self.r = np.dot(x, self.W) + self.b
        self.o = self.non_linearity(self.r)
        return self.o

    def backward(self, delta):
        delta = np.dot(delta, self.non_linearity_pr(self.r))

        db = delta
        dw = np.outer(self.x, delta)
        delta = np.dot(delta, self.W.T)

        self.W -= self.learning_rate * (dw + 0.001 * self.W.mean())
        self.b -= self.learning_rate * db

        return delta
