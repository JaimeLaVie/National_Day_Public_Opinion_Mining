# import re
from collections import defaultdict

# import jieba
import numpy as np
# from jieba import posseg
import datetime

# ################################################
# classifier based on Support Vector Machine
# ################################################
from sklearn.svm import SVC
from sklearn.externals import joblib

class SVMClassifier:
    def __init__(self, train_data, train_labels, best_words, C):
        train_data = np.array(train_data)
        train_labels = np.array(train_labels)

        self.best_words = best_words
        self.clf = SVC(C=C)            # Soft-Margin SVM
        self.__train(train_data, train_labels)

    def words2vector(self, all_data):
        vectors = []

        best_words_index = {}
        for i, word in enumerate(self.best_words):
            best_words_index[word] = i
        # print ("best_words_index is ", best_words_index)

        for data in all_data:
            vector = [0 for x in range(len(self.best_words))]
            for word in data:
                i = best_words_index.get(word)
                if i is not None:
                    vector[i] = vector[i] + 1
            vectors.append(vector)

        vectors = np.array(vectors)
        return vectors

    def __train(self, train_data, train_labels):
        print("SVMClassifier is training ...... ")

        train_vectors = self.words2vector(train_data)

        self.clf.fit(train_vectors, np.array(train_labels))

        joblib.dump(self.clf, "model/svm_rele.m")

        print("SVMClassifier trains over!")

    def classify(self, data):
        vector = self.words2vector([data])

        prediction = self.clf.predict(vector)
        # result = str(prediction) + str(label) + str(data) +'\n'
        # with open('f_runout/prediction_%s.txt'%(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")),"a", encoding = 'UTF-8') as f:
        #     f.write(result)

        return prediction[0]




