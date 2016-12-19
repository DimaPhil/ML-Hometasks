import numpy as np


def sigmoid(x):
    return 1. / (1 + np.exp(-x))


def sigmoid_der(x):
    s = sigmoid(x)
    return np.diag(s * (1 - s))


def soft_max(x):
    return np.exp(x) / np.exp(x).sum()


def soft_max_der(x):
    p = soft_max(x)
    t = np.outer(p, p)
    return np.diag(p) - t
