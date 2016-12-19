import numpy as np
import Layer as l
import functions

default_learning_rate = 0.1


def create_net():
    net = [
        l.Layer((784, 256), functions.sigmoid, functions.sigmoid_der, default_learning_rate),
        l.Layer((256, 128), functions.sigmoid, functions.sigmoid_der, default_learning_rate),
        l.Layer((128, 64), functions.sigmoid, functions.sigmoid_der, default_learning_rate),
        l.Layer((64, 10), functions.soft_max, functions.soft_max_der, default_learning_rate),
    ]
    return net


def train(net, x, y):
    _x = x
    for layer in net:
        _x = layer.forward(_x)
    delta = np.zeros(10)
    delta[y] = -1.0 / _x[y]
    loss = -np.log(_x[y])
    for layer in net[::-1]:
        delta = layer.backward(delta)
    return loss


def predict(net, x):
    _x = x
    for layer in net:
        _x = layer.forward(_x)
    return np.argmax(_x)


def accuracy(net, xs, ys):
    cnt = 0
    for x, y in zip(xs, ys):
        if predict(net, x) == y:
            cnt += 1
    return cnt / len(xs)


def aligned(x):
    s = str(x)
    while len(s) < 5:
        s += ' '
    return s


def show_stats(x_valid, y_valid, net):
    failed = [[0 for i in range(10)] for j in range(10)]
    for x, y in zip(x_valid, y_valid):
        py = predict(net, x)
        if py != y:
            failed[py][y] += 1
    print('predicted\\actual')
    print('\n'.join(' '.join(map(aligned, element)) for element in failed))
