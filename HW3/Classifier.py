from collections import Counter
import glob
import numpy as np

class Message:
    def __init__(self, text):
        subject, _, body = tuple(text.splitlines())
        self.subject = tuple([int(i) for i in subject.split()[1:]])
        self.body = tuple([int(i) for i in body.split()])

    def __iter__(self):
        return iter(self.subject*0 + self.body)

folds = []
for part in glob.glob('data/Bayes/pu1/*'):
    cur_dataset = {0: [], 1: []}
    for msg_file in glob.glob(part + '/*'):
        with open(msg_file, 'r') as data:
            label = 1 if 'spmsg' in msg_file else 0
            cur_dataset[label].append(Message(data.read()))
            folds.append(cur_dataset)

class SpamClassifier:
    def __init__(self, data, h=1.0):
        assert len(data) == 2 and 0 in data and 1 in data
        total = sum(len(i) for i in data.values())
        label_probability = {label: len(messages)/total for label, messages in data.items()}
        self.label_probability = label_probability
        assert min(label_probability.values()) > 0
        vocab = Counter()
        self.vocab = vocab
        for ms in data.values():
            for m in ms:
                vocab.update(m)
        probabilities = {label: {} for label in data}
        self.probabilities = probabilities
        for label, ms in data.items():
            counter = Counter()
            for m in ms:
                counter.update(m)
            total = sum(counter.values()) + len(vocab)
            for w in vocab:
                probabilities[label][w] = (counter[w] + 1)/total
        self.threshold = 0
        best_threshold = (self.threshold, self.score(data))
        tmp = np.array([(self.predict(m, True)[1], 0) for m in data[0]] + [(self.predict(m, True)[1], 1) for m in data[1]])
        for t in np.arange(0, 1, 0.01):
             tp = ((tmp[:, 0]>=t) * (tmp[:,1])).sum()
             tn = ((tmp[:, 0]<t) * (1-tmp[:,1])).sum()
             fp = ((tmp[:, 0]>=t) * (1-tmp[:,1])).sum()
             fn = ((tmp[:, 0]<t) * (tmp[:,1])).sum()
             s = (tp+tn)/(tp+fp+tn+fn)
             if fp / (tn + fp) <= h and s >= best_threshold[1]:
                 best_threshold = (t, s)
        self.threshold = best_threshold[0]
        _, tp, tn, fp, fn = self.score(data, True)
        print(tp, fn)
        print(fp, tn)

    def score(self, data, full=False):
        assert len(data) == 2 and 0 in data and 1 in data
        tmp = np.array([(self.predict(m, True)[1], 0) for m in data[0]] + [(self.predict(m, True)[1], 1) for m in data[1]])
        t = self.threshold
        tp = ((tmp[:, 0]>=t) * (tmp[:,1])).sum()
        tn = ((tmp[:, 0]<t) * (1-tmp[:,1])).sum()
        fp = ((tmp[:, 0]>=t) * (1-tmp[:,1])).sum()
        fn = ((tmp[:, 0]<t) * (tmp[:,1])).sum()
        if full:
            return (tp + tn)/(tp+tn+fp+fn), tp, tn, fp, fn
        return (tp + tn)/(tp+tn+fp+fn)

    def predict(self, message, return_prob=False):
        score = {}
        for label in self.probabilities:
            score[label] = np.log(self.label_probability[label])
            score[label] += sum(np.log(self.probabilities[label][w]) for w in message if w in self.vocab)
        assert score[1] < 0 and score[0] < 0
        p = score[1]/score[0]
        p = np.exp(1-p)/(1+np.exp(1-p))
        ans = 1 if p >= self.threshold else 0
        if return_prob:
            return ans, p
        return ans

def merge(ds):
    res = {}
    for d in ds:
        res.update(d.items())
    return res

s = 0
a,b,c,d = 0,0,0,0
for i in range(len(folds)):
    train = folds[i]
    classifier = SpamClassifier(train, 0.05)
    s1, a1, b1, c1, d1 = classifier.score(merge(folds[:i] + folds[i+1:]), True)
    s += s1
    a+=a1
    b+=b1
    c+=c1
    d+=d1
print(c/(a+b+c+d))
print(b/(a+b+c+d))
print(s/len(folds))
print((a+b)/(a+b+c+d))
