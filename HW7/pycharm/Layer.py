import numpy as np

lam = 0.001


class Layer:
    def __init__(self, shape, nonlinearity, nonlinearity_der, learning_rate):
        self.W = np.random.normal(0, 0.02, shape)
        self.b = np.random.normal(0, 0.02, shape[1])
        self.nonlinearity = nonlinearity
        self.nonlinearity_der = nonlinearity_der
        self.learning_rate = learning_rate;

    def forward(self, x):
        self.x = x
        self.r = np.dot(x, self.W) + self.b
        self.o = self.nonlinearity(self.r)
        return self.o

    def backward(self, delta):
        delta = np.dot(delta, self.nonlinearity_der(self.r))

        dB = delta
        dW = np.outer(self.x, delta)
        delta = np.dot(delta, self.W.T)

        self.W -= self.learning_rate * (dW + lam * self.W.mean())
        self.b -= self.learning_rate * dB

        return delta
