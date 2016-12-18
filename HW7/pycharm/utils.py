import numpy as np
import Layer as l
import functions as f

default_learning_rate = 0.1


def create_net():
    net = [
        l.Layer((784, 256), f.sigmoid, f.sigmoid_der, default_learning_rate),
        l.Layer((256, 128), f.sigmoid, f.sigmoid_der, default_learning_rate),
        l.Layer((128, 64), f.sigmoid, f.sigmoid_der, default_learning_rate),
        l.Layer((64, 10), f.softmax, f.softmax_der, default_learning_rate),
    ]
    return net


def train(net, x, y):
    o = x
    for layer in net:
        o = layer.forward(o)
    delta = np.zeros(10)
    delta[y] = -1. / o[y]
    loss = -np.log(o[y])
    for layer in net[::-1]:
        delta = layer.backward(delta)
    return loss


def predict(net, x):
    o = x
    for layer in net:
        o = layer.forward(o)
    return np.argmax(o)


def accuracy(net, X, Y):
    c = 0
    for x, y in zip(X, Y):
        if predict(net, x) == y:
            c += 1
    return c / len(X)
