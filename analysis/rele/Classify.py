import os
import re
import numpy as np
from sklearn.externals import joblib

Basic_Path = os.getcwd()

class classify:
    def __init__(self, type_, text, basic_path):
        self.type = type_
        self.text = text
        self.basic_path = basic_path

        self.best_words = []
        with open (self.basic_path + "/bestwords.txt","r", encoding = 'UTF-8') as f:
            for lines in f:
                self.best_words.append(lines.replace("\n", ""))
        # print (self.best_words)

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

    def get_keywords(self, keywordpath):
        root_path = os.path.dirname(os.path.abspath(__file__))
        keywordpath = os.path.normpath(os.path.join(root_path, keywordpath))

        keywords_list = []
        with open(keywordpath, encoding="utf-8") as f:
            for line in f:
                # keywords_splits = keyword_split.split(line.strip())
                keyword = line.replace('\n', '')
                keywords_list.append(keyword)

            return keywords_list

    def Classify(self):

        self.clf = joblib.load(self.basic_path + "/model/svm_rele.m")

        # from corpus import get_keywords
        keywords_list = self.get_keywords(self.basic_path + '/data/rele_keywords.txt')
        irrewords_list = self.get_keywords(self.basic_path + '/data/rele_irrewords.txt')

        isKeywords = 0
        isIrrewords = 0
        for words in keywords_list:
            isKeyword = re.findall(str(words), (self.text))
            if len(isKeyword) != 0:
                # print ('isKeyword = ', isKeyword)
                isKeywords += len(isKeyword)
        for words in irrewords_list:
            isIrreword = re.findall(str(words), (self.text))
            if len(isIrreword) != 0:
                # print ('isIrreword = ', isIrreword)
                isIrrewords += len(isIrreword)
        if isKeywords > isIrrewords:
            prediction = 1
        elif isKeywords < isIrrewords:
            prediction = 0
        else:
            vector = self.words2vector([self.text])
            prediction = self.clf.predict(vector)[0]
        # print ("prediction: ", prediction)

        return prediction
            

def test_twitter_rele(text, basic_path = Basic_Path):
    type_ = "twitter_rele"

    test = classify(type_, text, basic_path)

    return test.Classify()


if __name__ == "__main__":
    # test_dict()
    # test_twitter_rele("RT @chinascio: Chinese #AirForce releases promo video to celebrate National Day. #PRC70 ")
    pass
