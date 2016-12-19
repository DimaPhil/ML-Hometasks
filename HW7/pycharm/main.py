import numpy as np
import utils
import draw

data = np.load('data/mnist.npz', 'rb')
(_, x_test), (_, x_train), (_, x_valid), (_, y_valid), (_, y_train), (_, y_test) = data.items()

net = utils.create_net()
losses = []
train_accuracies = []
valid_accuracies = []

best_valid_accuracy = 0

for k in range(10):
    print('k =', k)
    failed = 0
    for i, (x, y) in enumerate(zip(x_train, y_train)):
        failed += utils.train(net, x, y)
    failed /= len(x_train)
    valid_accuracy = utils.accuracy(net, x_valid, y_valid)
    train_accuracy = utils.accuracy(net, x_train, y_train)

    losses.append(failed)
    valid_accuracies.append(valid_accuracy)
    train_accuracies.append(train_accuracy)
    if valid_accuracy > best_valid_accuracy:
        best_valid_accuracy = valid_accuracy

    print('failed:', failed)
    print('valid accuracy:', valid_accuracy)
    print('train accuracy:', train_accuracy)
    utils.show_stats(x_valid, y_valid, net)

draw.draw(x_valid, y_valid, net)
