import knn
import visualizer
from metrics import Metrics as ms
from transformations import Transformations as ts


def main():
    xs, ys, values = knn.load('chips.txt')
    for metric, ms_comment in ms.get_all_metrics(ms):
        for transform, ts_comment in ts.get_all_transformations(ts):
            for k in range(10, 5, -1):
                print('Processing metric \"' + ms_comment + '\", transformation = \"' + ts_comment + '\", k = ' + str(k) + '...')
                new_space = transform(xs, ys)
                train, test = knn.fold_cross_validation(new_space, values, metric, 10, k, 10)
                print(test)
                print(train)
                #if len(train[0]) == 3:
                #    visualizer.draw(train, 25)
                #    visualizer.draw(test, 100)
                #    visualizer.finalize()

if __name__ == '__main__':
    main()