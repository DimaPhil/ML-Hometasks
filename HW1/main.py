import knn
import visualizer
from metrics import Metrics as ms
from transformations import Transformations as ts


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


def main():
    xs, ys, values = load('chips.txt')
    xs, ys = ts.normalization(xs, ys)
    for metric, ms_comment in ms.get_all_metrics(ms)[1:]:
        for transform, ts_comment in ts.get_all_transformations(ts)[1:]:
            for bestk in range(15, 4, -1):
                new_space = transform(xs, ys)
                print(
                'Processing metric \"' + ms_comment + '\", transformation = \"' + ts_comment + '\", t = 10, k = 10, bestk = ' + str(bestk) + '...')
                train, test, error = knn.fold_cross_validation(new_space, values, metric, 10, 10, bestk)
                print('Average error: ' + str(error) + '%')
                print(test)
                print(train)


if __name__ == '__main__':
    main()