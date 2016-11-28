import math


def load(filename):
    data = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            _, x, y = map(float, line.split(';'))
            data.append([x, y])
    return data


def MSE(real, answer):
    sum = 0.0
    for i in range(len(real)):
        sum += math.pow(real[i][1] - answer[i][1], 2)
    return sum / len(real)
