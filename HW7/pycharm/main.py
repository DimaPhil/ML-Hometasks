import numpy as np
import utils as u
import pickle
import draw

data = np.load('data/mnist.npz', 'rb')
# print(data.keys())
(_, x_test), (_, x_train), (_, x_valid), (_, y_valid), (_, y_train), (_, y_test) = data.items()

net = u.create_net()
losses = []
train_accs = []
valid_accs = []

best_valid = 0

for k in range(10):
    print('k =', k)
    loss = 0
    for i, (x, y) in enumerate(zip(x_train, y_train)):
        loss += u.train(net, x, y)
    loss /= len(x_train)
    valid_acc = u.accuracy(net, x_valid, y_valid)
    train_acc = u.accuracy(net, x_train, y_train)

    losses.append(loss)
    valid_accs.append(valid_acc)
    train_accs.append(train_acc)
    if valid_acc > best_valid:
        best_valid = valid_acc
        # with open('net.pkl', 'wb') as out:
        #    pickle.dump(net, out)

    print('epoch:', k)
    print('loss:', loss)
    print('valid acc:', valid_acc)
    print('train acc:', train_acc)

draw.draw(x_valid, y_valid, net)
