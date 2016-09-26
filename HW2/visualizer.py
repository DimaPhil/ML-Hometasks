from matplotlib import pyplot as plt
from matplotlib import lines as lns


def draw(data, labels, a, b, size=25):
    plt.scatter(data,
                labels,
                s=size)
    plt.plot([0, 1], [a, a + b])

def finalize():
    plt.show()
