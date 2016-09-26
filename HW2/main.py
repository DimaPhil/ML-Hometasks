from cross_validation import CrossValidation
import gradient
import genetic_algo
import visualizer


def load(filename):
    data = []
    labels = []
    with open(filename, 'r') as input:
        for line in input.readlines():
            characteristics = list(map(int, line.split(',')))
            assert len(characteristics) == 3
            data.append(characteristics[:-1])
            labels.append(characteristics[-1])
    print(str(len(data)) + ' elements loaded from ' + filename)
    return data, labels

mn = [0 for i in range(2)]
mx = [0 for j in range(2)]
mnl = float('inf')
mxl = -float('inf')


def normalize_data(data):
    for i in range(len(data[0])):
        mn[i] = float('inf')
        mx[i] = -float('inf')
        for j in range(len(data)):
            mn[i] = min(mn[i], data[j][i])
            mx[i] = max(mx[i], data[j][i])
        for j in range(len(data)):
            data[j][i] = (data[j][i] - mn[i]) / (mx[i] - mn[i])
    return data


def normalize_labels(labels):
    global mnl, mxl
    mnl = float('inf')
    mxl = -float('inf')
    for i in range(len(labels)):
        mnl = min(mnl, labels[i])
        mxl = max(mxl, labels[i])
    for i in range(len(labels)):
        labels[i] = (labels[i] - mnl) / (mxl - mnl)
    return labels


def find_mean(data, labels, w):
    ans = 0
    for id, obj in enumerate(data):
        cost = w[0]
        for i in range(len(obj)):
            cost += w[i + 1] * obj[i]
        ans += (cost - labels[id]) ** 2
    return ans / len(data)


def predict(data, w):
    data[0] = (data[0] - mn[0]) / (mx[0] - mn[0])
    data[1] = (data[1] - mn[1]) / (mx[1] - mn[1])

    cost = w[0]
    for i in range(len(data)):
        cost += w[i + 1] * data[i]
    return cost * (mxl - mnl) + mnl


def main():
    data, labels = load('prices.txt')
    data = normalize_data(data)
    labels = normalize_labels(labels)
    train, test = CrossValidation(data, 10).divide(0)
    w = gradient.learn(train, labels)
    print(w)
    visualizer.draw([e[0] for e in data], labels, w[0], w[1])
    visualizer.finalize()
    visualizer.draw([e[1] for e in data], labels, w[0], w[2])
    visualizer.finalize()
    print('Dataset trained, waiting for input...')
    mean = find_mean(test, labels, w) * (mxl - mnl) + mnl
    print('Mean = ' + str(mean))
    while True:
        x, y = map(int, input().split())
        print('Predicted cost: ' + str(predict([x, y], w)))

if __name__ == '__main__':
    main()