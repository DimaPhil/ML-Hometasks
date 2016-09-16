from matplotlib import pyplot as plt


def draw(data, size=50):
    cs = ['#FFFFFF', '#FF0000', '#808080', '#800000']
    plt.scatter([point[0] for point in data],
                [point[1] for point in data],
                c=[cs[point[2]] for point in data],
                s=size)


def finalize():
    plt.show()
