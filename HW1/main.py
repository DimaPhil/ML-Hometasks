import knn
import visualizer
from metrics import Metrics as ms

def main():
    xs, ys, values = knn.load('chips.txt')
    #visualizer.draw(xs, ys, values)
    for metric in ms.get_all_metrics(ms):
        knn.fold_cross_validation(xs, ys, values, metric)

if __name__ == '__main__':
    main()