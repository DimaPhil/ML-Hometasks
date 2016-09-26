import random

def learn(data, labels):
    EPS = 10 ** (-9)
    for i in range(len(data)):
        data[i] = [-1.] + data[i]
    w = [0. for i in range(len(data[0]))]
    for i in range(len(w)):
        w[i] = random.random()
    alpha = 0.1
    while True:
        error = 0.
        for id, obj in enumerate(data):
            h = 0.
            for i in range(len(w)):
                h += w[i] * obj[i]
            error += (h - labels[id]) ** 2
        error /= 2 * len(data)
        #error = math.sqrt(error)

        nw = [0. for _ in range(len(w))]
        for k in range(len(nw)):
            step = 0
            for id, obj in enumerate(data):
                h = 0
                for i in range(len(w)):
                    h += w[i] * obj[i]
                step += (h - labels[id]) * obj[k]
            nw[k] = w[k] - step * alpha / len(data)
        difference = 0
        for i in range(len(w)):
            difference += abs(w[i] - nw[i])
        #print('difference = ' + str(difference))
        if difference < EPS:
            break
        w = list(nw)
    return w


