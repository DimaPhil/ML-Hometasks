import random
from functools import cmp_to_key


def error_function(data, labels, w):
    error = 0
    for id, obj in enumerate(data):
        h = w[0]
        for i in range(len(obj)):
            h += w[i + 1] * obj[i]
        error += (h - labels[id]) ** 2
    error /= len(data)
    return error


def learn(data, labels):
    ws = [[1. for i in range(len(data[0]) + 1)]]
    ITERATIONS = 100
    MAX_VECTORS = 50
    for it in range(ITERATIONS):
        size = len(ws)
        for i in range(size):
            w = ws[i]
            nw = list(w)
            for i in range(len(w)):
                if random.randint(1, 2) == 1:
                    nw[i] += random.random()
                else:
                    nw[i] -= random.random()
            ws.append(nw)
        ws = sorted(ws, key=cmp_to_key(lambda w1, w2: error_function(data, labels, w1) - error_function(data, labels, w2)))
        ws = ws[:MAX_VECTORS]
        print(list(error_function(data, labels, w) for w in ws))
    print(ws[0])
    print(error_function(data, labels, ws[0]))
    return ws[0]

