import knn
import visualizer
from metrics import Metrics as ms


def main():
    xs, ys, values = knn.load('chips.txt')
    for metric in ms.get_all_metrics(ms):
        train, test = knn.fold_cross_validation(xs, ys, values, metric, 10, 10, 1)
        print(test)
        print(train)
        visualizer.draw(train, 25)
        visualizer.draw(test, 100)
        visualizer.finalize()

if __name__ == '__main__':
    main()