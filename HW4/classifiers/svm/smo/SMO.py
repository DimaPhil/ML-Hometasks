import random

random.seed('ML-lab04')

class SMO:
    EPSILON = 10 ** (-3)

    class SMOSolution:
        def __init__(self, n):
            self.alphas = [0.0 for _ in range(n)]
            self.b = 0.0

    def E(self, point, points, alphas, b, kernel):
        f = 0.0
        for i in range(len(points)):
            x = points[i]
            value = -1 if x[-1] == 0 else 1
            f += alphas[i] * value * kernel(x[:-1], point[:-1])
        value = -1 if point[-1] == 0 else 1
        return f + b - value

    def solve(self, train, parameters):
        m = len(train)
        c = parameters.c
        tol = parameters.tol
        s = self.SMOSolution(m)
        passes = 0
        while passes < parameters.maxPasses:
            numChangedAlphas = 0
            for i in range(m):
                x = train[i]
                valuex = -1 if x[:-1] == 0 else 1
                Ei = self.E(x, train, s.alphas, s.b, parameters.kernel)
                if (valuex * Ei < -tol and s.alphas[i] < c) or (valuex * Ei > tol and s.alphas[i] > 0.0):
                    j = random.randint(0, m - 1)
                    while j == i:
                        j = random.randint(0, m - 1)
                    y = train[j]
                    Ej = self.E(y, train, s.alphas, s.b, parameters.kernel)
                    oldAi = s.alphas[i]
                    oldAj = s.alphas[j]
                    L = 0
                    H = 0
                    if x[-1] == y[-1]:
                        L = max(0.0, s.alphas[i] + s.alphas[j] - c)
                        H = min(c, s.alphas[i] + s.alphas[j])
                    else:
                        L = max(0.0, s.alphas[j] - s.alphas[i])
                        H = min(c, c + s.alphas[j] - s.alphas[i])
                    if abs(H - L) <= self.EPSILON:
                        continue
                    eta = 2 * parameters.kernel(x[:-1], y[:-1]) - parameters.kernel(x[:-1], x[:-1]) - parameters.kernel(y[:-1], y[:-1])
                    if eta >= 0:
                        continue
                    valuey = -1 if y[-1] == 0 else 1
                    s.alphas[j] -= (valuey * (Ei - Ej)) / eta
                    if s.alphas[j] > H:
                        s.alphas[j] = H
                    elif s.alphas[j] < L:
                        s.alphas[j] = L

                    if abs(s.alphas[j] - oldAj) < self.EPSILON:
                        continue
                    s.alphas[i] += valuex * valuey * (oldAj - s.alphas[j])

                    b1 = s.b - Ei - valuex * (s.alphas[i] - oldAi) * parameters.kernel(x[:-1], x[:-1]) -\
                         valuey * (s.alphas[j] - oldAj) * parameters.kernel(x[:-1], y[:-1])
                    b2 = s.b - Ej - valuex * (s.alphas[i] - oldAi) * parameters.kernel(x[:-1], y[:-1]) -\
                         valuey * (s.alphas[j] - oldAj) * parameters.kernel(y[:-1], y[:-1])

                    if 0 < s.alphas[i] < c:
                        s.b = b1
                    elif 0 < s.alphas[j] < c:
                        s.b = b2
                    else:
                        s.b = (b1 + b2) / 2.0

                    numChangedAlphas += 1

            if numChangedAlphas == 0:
                passes += 1
            else:
                passes = 0
        return s