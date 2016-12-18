import numpy as np


def sigmoid(x):
    return 1. / (1 + np.exp(-x))


def sigmoid_der(x):
    s = sigmoid(x)
    return np.diag(s * (1 - s))


def softmax(x):
    return np.exp(x) / np.exp(x).sum()


def softmax_der(x):
    p = softmax(x)
    t = np.outer(p, p)
    return np.diag(p) - t
