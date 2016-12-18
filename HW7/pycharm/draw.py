import matplotlib.pyplot as plt
import numpy as np
import utils as u


def draw(x_valid, y_valid, net):
    c = 0
    errors = []
    pics = []
    for x, y in zip(x_valid, y_valid):
        py = u.predict(net, x)
        if py != y:
            errors.append((py, y))
            pics.append(x)
    # errors[:10]
    for x, err in zip(pics[:10], errors[:10]):
        x = np.uint8(x * 255)
        x = x.reshape((28, 28))
        print(err)
        plt.imshow(x, cmap='gray')
        plt.show()
