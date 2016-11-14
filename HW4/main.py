from Utils import *
from classifiers.knn.KNN import KNN
from classifiers.svm.SVM import SVM
from classifiers.parameters.Measures import Measures
from classifiers.dividers.Divider import Divider
from functools import cmp_to_key
import math

def main():
    data = loadData('chips.txt')
    print('Running KNN...')
    knn_instance = KNN(data)
    knn_parameters = knn_instance.learn(data, Measures(1))
    print('Finished KNN: ' + str(knn_parameters.accuracy))
    print('Running SVM...')
    svm_instance = SVM(data)
    svm_parameters = svm_instance.learn(data, Measures(1))
    print('Finished SVM: ' + str(svm_parameters.accuracy))

    class Score:
        def __init__(self, value, method, index):
            self.value = value
            self.method = method
            self.index = index

    divider = Divider(data, 7)
    svm_scores = []
    knn_scores = []

    i = 0
    D = divider.divided[0]
    answerD = knn_instance.evaluate(D[0], D[1], knn_parameters)
    knnDError = knn_parameters.measure.get(D[1], answerD)

    knnP = 0.0
    print(len(divider.divided))
    for div in divider.divided:
        answer = knn_instance.evaluate(div[0], div[1], knn_parameters)
        knn_score = Score(knn_parameters.measure.get(div[1], answer), "KNN", i)
        knn_scores.append(knn_score)
        answer = svm_instance.evaluate(div[0], div[1], svm_parameters)
        if knn_score.value >= knnDError:
            knnP += 1
        svm_score = Score(svm_parameters.measure.get(div[1], answer), "SVM", i)
        svm_scores.append(svm_score)
        i += 1
    knnP /= (len(divider.divided) + 2)
    n = len(knn_scores)
    m = n
    print("n = " + str(n))
    zipped = zip(list(map(lambda x: x.value * 4, knn_scores)), list(map(lambda x: x.value * 4, svm_scores)))
    pvalue = 0.0
    for e in zipped:
        pvalue += (e[0]**2 - e[1]**2) / e[0]

    print("KNN p-value: " + str(pvalue))

    vars = []
    for i in range(len(knn_scores)):
        vars.append([abs(knn_scores[i].value - svm_scores[i].value), -1 if knn_scores[i].value < svm_scores[i].value else 1, i + 1])
    vars = sorted(vars, key=cmp_to_key(lambda x, y: x[0] - y[0]))

    #rx = map(lambda e: vars.index(e), knn_scores)
    #ry = map(lambda e: vars.index(e), svm_scores)
    #Rx = sum(rx)
    #Ry = sum(ry)
    #W = Rx
    W = 0
    for i in range(len(vars)):
        W += vars[i][1] * vars[i][2]
    print("W = " + str(W))
    #alpha = 0.95 # importance
    #Fa = 1.960   # quantile (1 - a / 2) of standard normal distribution
    #Wc = (W - m * (m + n + 1.0) / 2.0) / (math.sqrt(m * n * (m + n + 1.0) / 2.0))
    #print("Wc = " + str(abs(Wc)))

    #Wcx = 0.5 * Wc * (1.0 + math.sqrt((n + n - 2.0) / (n + m - 1.0 - Wc * Wc)))

    #xa = 1.645
    #ya = 2.1448
    #print("Wcx = " + str(abs(Wcx)))

if __name__ == '__main__':
    main()
