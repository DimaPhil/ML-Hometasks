import matplotlib.pyplot as plt
import numpy as np
import utils


def draw(x_valid, y_valid, net):
    errors = []
    pics = []
    for x, y in zip(x_valid, y_valid):
        py = utils.predict(net, x)
        if py != y:
            errors.append((py, y))
            pics.append(x)
    for x, err in zip(pics[:10], errors[:10]):
        x = np.uint8(x * 255)
        x = x.reshape((28, 28))
        (py, y) = err
        print(py, 'predicted, but there is', y)
        plt.imshow(x, cmap='gray')
        plt.show()
