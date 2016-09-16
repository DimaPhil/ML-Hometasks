import random
from functools import cmp_to_key

random.seed('ML-HW1')


def load(filename):
    with open(filename, 'r') as input:
        xs = []
        ys = []
        values = []
        for line in input.readlines():
            x, y, value = line.strip().split(',')
            xs.append(float(x))
            ys.append(float(y))
            values.append(int(value))
        assert (len(xs) == len(ys) and len(ys) == len(values))
        print(str(len(xs)) + ' objects loaded from ' + filename)
        return xs, ys, values


def fold_cross_validation(xs, ys, values, metric, t=10, k=10, bestk=1):
    n = len(xs)
    best_accuracy = 0.
    best_train = []
    best_test = []
    for _ in range(t):
        ids = [i for i in range(n)]
        random.shuffle(ids)
        blocks = []
        for j in range(0, n, k):
            block = [[xs[ids[i]], ys[ids[i]], values[ids[i]]] for i in range(j, min(n, j + k))]
            blocks.append(block)
        for i, block in enumerate(blocks):
            other = [_i for _i in range(len(blocks))]
            other.remove(i)
            train = []
            for other_block in other:
                train.extend(blocks[other_block])
            successful = 0
            test = []
            for test_data in blocks[i]:
                train = sorted(train, key=cmp_to_key(lambda x, y: (metric([x[0], x[1]], [test_data[0], test_data[1]]) -
                                                                   metric([y[0], y[1]], [test_data[0], test_data[1]]))))
                # sorting validation
                for cid in range(len(train) - 1):
                    m1 = metric([train[cid][0], train[cid][1]], [test_data[0], test_data[1]])
                    m2 = metric([train[cid + 1][0], train[cid + 1][1]], [test_data[0], test_data[1]])
                    assert (m1 <= m2)

                best = train[:bestk]
                cnt_zero = len(list(filter(lambda e: e[2] == 0, best)))
                cnt_one = len(list(filter(lambda e: e[2] == 1, best)))
                predicted_answer = 1 if cnt_one > cnt_zero else 0
                if predicted_answer == test_data[2]:
                    successful += 1
                test.append(
                    [test_data[0], test_data[1], test_data[2] + (0 if predicted_answer == test_data[2] else 2)])
            accuracy = successful * 1. / len(blocks[i])
            if best_accuracy < accuracy:
                best_accuracy = accuracy
                best_train = train
                best_test = test
    print('We are fucking awesome, accuracy: ' + str(best_accuracy * 100.) + '%')
    return best_train, best_test
