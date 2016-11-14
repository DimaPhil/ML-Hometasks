class ConfusionMatrix:
    def __init__(self, real, answer):
        self.matrix = [[0, 0], [0, 0]]
        self.p = 0
        self.n = 0
        for i in range(len(real)):
            self.matrix[answer[i][2]][real[i][2]] += 1
            if real[i][2] == 1:
                self.p += 1
            else:
                self.n += 1

    def tp(self):
        return self.matrix[1][1]

    def fn(self):
        return self.matrix[0][1]

    def tn(self):
        return self.matrix[0][0]

    def fp(self):
        return self.matrix[1][0]

    def p(self):
        return self.p

    def n(self):
        return self.n
