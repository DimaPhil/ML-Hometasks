from BayesClassifier import BayesClassifier


def main():
    a, b = BayesClassifier().learn()
    print(a, b)

if __name__ == '__main__':
    main()