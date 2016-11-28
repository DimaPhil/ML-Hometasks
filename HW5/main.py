import Utils
from KernelNPRegression import KernelNPRegression
from RobustNPRegression import RobustNPRegression
from matplotlib import pyplot as plt

def draw_scatter(points, color):
    plt.scatter([point[0] for point in points],
             [point[1] for point in points],
             c=color)


def draw_graphic(points, color):
    plt.plot([point[0] for point in points],
             [point[1] for point in points],
             c=color)


def main():
    data = Utils.load('data.csv')
    kernel_regression_instance = KernelNPRegression(data)
    robust_regression_instance = RobustNPRegression(data)
    print('Running KernelNonParametristicRegression...')
    kernel_parameters = kernel_regression_instance.learn(data)
    print('Finished, parameters:\n' + str(kernel_parameters))
    print('Running RobustNonParametristicRegression...')
    robust_parameters = robust_regression_instance.learn(data)
    print('Finished, parameters:\n' + str(robust_parameters))

    delta = 0.05
    points = []
    for di in data:
        points.append(list(di))
    draw_scatter(points, 'green')
    points = []
    minx = min(map(lambda p: p[0], data))
    maxx = max(map(lambda p: p[0], data))
    p = minx
    while p < maxx:
        points.append(kernel_regression_instance.evaluate([p, 0.0], kernel_parameters))
        p += delta
    draw_graphic(points, 'red')
    #plt.show()

    #points = []
    #for di in data:
    #    points.append(list(di))
    #draw_scatter(points, 'green')
    points = []
    minx = min(map(lambda p: p[0], data))
    maxx = max(map(lambda p: p[0], data))
    p = minx
    while p < maxx:
        points.append(robust_regression_instance.evaluate([p, 0.0], robust_parameters))
        p += delta
    draw_graphic(points, 'blue')
    plt.show()

if __name__ == '__main__':
    main()