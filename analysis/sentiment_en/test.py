import datetime
from multiprocessing import Process

from feature_extraction import ChiSquare
from tools import get_accuracy
from tools import Write2File
import re
import os


class Test:
    def __init__(self, type_, train_num, test_num, feature_num, max_iter, C, k, corpus):
        self.type = type_
        self.train_num = train_num
        self.test_num = test_num
        self.feature_num = feature_num
        self.max_iter = max_iter
        self.C = C
        self.k = k
        self.parameters = [train_num, test_num, feature_num]

        # get the f_corpus
        self.train_data, self.train_labels = corpus.get_train_corpus(train_num)
        # print ('self.train_data length: ', len(self.train_data), 'self.train_labels length: ', len(self.train_labels))
        self.test_data, self.test_labels = corpus.get_test_corpus(test_num)
        # print ('self.test_data length: ', len(self.test_data), 'self.test_labels length: ', len(self.test_labels))

        # feature extraction
        fe = ChiSquare(self.train_data, self.train_labels)
        self.best_words = fe.best_words(feature_num)

        with open('bestwords.txt',"w", encoding = 'UTF-8') as f:
            for words in self.best_words:
                f.write(words+'\n')

        self.single_classifiers_got = False

        self.precisions = [[0, 0],  # bayes
                           [0, 0],  # maxent
                           [0, 0]]  # svm

    def write(self, filepath, classify_labels, i=-1):
        results = get_accuracy(self.test_labels, classify_labels, self.parameters)
        if i >= 0:
            self.precisions[i][0] = results[10][1] / 100
            self.precisions[i][1] = results[7][1] / 100

        Write2File.write_contents(filepath, results)
    
    def test_sentiment_dict_svm(self):
        print("SVMClassifier")
        print("---" * 30)
        print("Train num = %s" % self.train_num)
        print("Test num = %s" % self.test_num)
        print("C = %s" % self.C)

        from classifiers import SVMClassifier
        svm = SVMClassifier(self.train_data, self.train_labels, self.best_words, self.C)

        from corpus import get_keywords
        keywords_list = get_keywords('data/sentiment_keywords.txt')
        # print (keywords_list)
        irrewords_list = get_keywords('data/sentiment_irrewords.txt')
        # print (irrewords_list)

        classify_labels = []
        print("Dict and SVM Classifier is testing ...")
        count = 0
        for data in self.test_data:
            isKeywords = 0
            isIrrewords = 0
            printkey = []
            printirre = []
            isNomeaning = re.findall('#', (data[0]))
            if len(isNomeaning) >= 5 or len(data) <= 4:
                prediction = 0
            else:
                for i in range (len(data)):
                    for words in keywords_list:
                        isKeyword = re.findall(str(words), (data[i]))
                        if len(isKeyword) != 0:
                            printkey.append(isKeyword)
                            # print ('isKeyword = ', isKeyword)
                            isKeywords += len(isKeyword)
                # print ('isKeywords = ', isKeywords)
                    for words in irrewords_list:
                        isIrreword = re.findall(str(words), (data[i]))
                        if len(isIrreword) != 0:
                            printirre.append(isIrreword)
                            # print ('isIrreword = ', isIrreword)
                            isIrrewords += len(isIrreword)
                if isKeywords > isIrrewords:
                    prediction = 1
                    # classify_labels.append(prediction)
                elif isKeywords < isIrrewords:
                    prediction = 0
                    # classify_labels.append(prediction)
                else:
                    prediction = svm.classify(data)
            classify_labels.append(prediction)
            result = str(prediction) + str(self.test_labels[count]) + str(isKeywords) + str(isIrrewords) + str(printkey) + str(printirre) + str(data) +'\n'
            with open('f_runout/prediction_%s.txt'%(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")),"a", encoding = 'UTF-8') as f:
                f.write(result)
            count += 1
        print("Dict and SVM Classifier tests over.")

        filepath = "f_runout/SVM-%s-train-%d-test-%d-f-%d-C-%d-%s-lin.xls" % \
                   (self.type,
                    self.train_num, self.test_num,
                    self.feature_num, self.C,
                    datetime.datetime.now().strftime(
                        "%Y-%m-%d-%H-%M-%S"))

        self.write(filepath, classify_labels, 2)

def test_twitter_sentiment():
    from corpus import TwitterCorpus

    type_ = "twitter_sentiment_en"
    train_num = 16
    test_num = 10
    feature_num = 5000
    max_iter = 50000
    C = 150
    k = 13
    # k = [1, 3, 5, 7, 9, 11, 13]
    corpus = TwitterCorpus()

    test = Test(type_, train_num, test_num, feature_num, max_iter, C, k, corpus)

    test.test_sentiment_dict_svm()


if __name__ == "__main__":
    # test_dict()
    test_twitter_sentiment()
