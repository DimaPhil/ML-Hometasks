from matplotlib import pyplot as plt
from matplotlib import colors as plc

def draw(xs, ys, values):
    colors = plc.ListedColormap(['#FF0000', '#FFFFFF'])
    data = [[[xs[i], ys[i]], 0 if values[i] == 1 else 1] for i in range(len(xs))]
    plt.scatter([point[0][0] for point in data],
                [point[0][1] for point in data],
                c=[point[1] for point in data],
                cmap=colors)
    plt.show()
