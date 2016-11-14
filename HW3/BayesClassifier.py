import os
import os.path
from message import Message
from collections import defaultdict
import math
import random


class BayesClassifier:
    def __init__(self):
        self.emails = []
        self.spam_frequency = defaultdict(int)
        self.ham_frequency = defaultdict(int)
        self.unique = 0
        self.spam_total = 0
        self.spam_total_probability = 0
        self.ham_total = 0
        self.ham_total_probability = 0

        for root, dirs, files in os.walk('.' + os.sep + 'pu1'):
            for file in files:
                self.head = []
                self.body = []
                is_spam = file.find('spmsg') != -1

                with open(os.path.join(root, file), 'r') as data:
                    lines = list(filter(lambda line: len(line.strip()) > 0, data.readlines()))
                    subject = lines[0]
                    self.head.extend(subject[len('Subject '):].split('\\s'))
                    self.head = list(filter(lambda s : len(s) > 0, self.head))
                    lines = lines[1:]
                    self.body.extend(lines)
                    final_body = list(self.head)
                    final_body.extend(self.body)
                    self.emails.append(Message(final_body, is_spam))

    def count_words_frequency(self, data, tests):
        spam_cnt = 0
        ham_cnt = 0
        word_tests = set()
        for e in tests:
            for w in e.get_body():
                word_tests.add(w)
        for email in data:
            if email.is_spam:
                spam_cnt += 1
            else:
                ham_cnt += 1

            for word in email.get_body():
                #if word not in word_tests:
                #    continue
                if email.is_spam:
                    self.spam_frequency[word] += 1
                else:
                    self.ham_frequency[word] += 1

        self.spam_total = 0
        self.spam_total_probability = 0
        self.ham_total = 0
        self.ham_total_probability = 0
        words = set()
        for word in self.spam_frequency.keys():
            self.spam_total += self.spam_frequency[word]
            words.add(word)
        for word in self.ham_frequency.keys():
            self.ham_total += self.ham_frequency[word]
            words.add(word)
        self.spam_total_probability = self.spam_total / len(self.emails)
        self.ham_total_probability = self.ham_total / len(self.emails)
        self.unique = len(words)

    def word_probability(self, cnt_table, word, total):
        return (cnt_table[word] + 1.0 / self.unique) / (total + 1)

    def find_measure(self, tests, b):
        tm = [[0, 0], [0, 0]]
        wrong = 0
        wrong2 = 0
        all = 0
        for email in tests:
            spam_probability = math.log(self.spam_total_probability)
            ham_probability = math.log(self.ham_total_probability)

            for word in email.get_body():
                spam_probability += math.log(self.word_probability(self.spam_frequency, word, self.spam_total))
                ham_probability += math.log(self.word_probability(self.ham_frequency, word, self.ham_total))
            #resClass = 1 if math.log(ham_probability / spam_probability) > 0.0001 else 0
            resClass = 0 if ham_probability > spam_probability else 1
            trueClass = 1 if email.is_spam else 0
            tm[resClass][trueClass] += 1
            all += 1
            if trueClass == 0 and resClass == 1:
                wrong += 0.1
            if trueClass == 1 and resClass == 0:
                wrong2 += 1
        print(str(int(wrong)) + '/' + str(all) + ' good letters went to spam')
        print(str(int(wrong2)) + '/' + str(all) + ' bad letters went to ham')

        if tm[1][1] == 0:
            print('NAN')
            return 0
        precision = tm[1][1] / (tm[1][1] + tm[1][0])
        recall = tm[1][1] / (tm[1][1] + tm[0][1])
        #accuracy = (tm[1][1] + tm[0][0]) / all

        #return accuracy
        return (1 + b * b) * precision * recall / (b * b * precision + recall)

    def learn(self):
        random.shuffle(self.emails)

        tests = self.emails[:len(self.emails) // 5]
        trains = self.emails[len(self.emails) // 5:]

        self.count_words_frequency(trains, tests)
        return self.find_measure(tests, 5), self.find_measure(trains, 5)
