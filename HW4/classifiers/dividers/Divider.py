import math
import random

random.seed('ML-lab04')

class Divider:
    def __init__(self, data, size):
        self.data = data
        self.divided = self.divide(size)

    def size(self):
        return len(self.divided)

    def divide(self, size):
        cv = self.crossValidation(len(self.data), size)
        train = cv[0]
        test = cv[1]
        result = []
        for i in range(len(train)):
            result.append([list(map(lambda i: self.data[i], train[i])),
                           list(map(lambda i: self.data[i], test[i]))])
        return result

    def crossValidation(self, dataSize, size):
        count = int(math.ceil(dataSize / size))
        index = [i for i in range(dataSize)]
        random.shuffle(index)
        train = []
        test = []
        for i in range(0, dataSize, count):
            tmpTrain = index[:i]
            tmpTest = []
            if i + count < dataSize:
                tmpTrain.extend(index[i + count:])
                tmpTest.extend(index[i:i + count])
            else:
                tmpTest.extend(index[i:])

            train.append(tmpTrain)
            test.append(tmpTest)
        return [train, test]