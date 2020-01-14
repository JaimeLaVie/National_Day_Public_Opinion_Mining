import os
import re
from random import shuffle


class Corpus:
    def __init__(self, filepath):
        root_path = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.normpath(os.path.join(root_path, filepath))

        re_split = re.compile("\0")

        self.pos_doc_list = []
        self.neg_doc_list = []
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                splits = re_split.split(line.strip())
                if splits[0] == '1':
                    self.pos_doc_list.append(splits[1:])
                elif splits[0] == '2':
                    self.neg_doc_list.append(splits[1:])
                else:
                    raise ValueError("Corpus Error")

        shuffle(self.pos_doc_list)
        shuffle(self.neg_doc_list)
        self.doc_length = len(self.pos_doc_list) + len(self.neg_doc_list)

        self.train_num = 0
        self.test_num = 0

        runout_content = "You are using the corpus: %s.\n" % filepath
        runout_content += "There are total %d positive and %d negative tweets." % \
                          (len(self.pos_doc_list), len(self.neg_doc_list))
        print(runout_content)

    def get_corpus(self, start=0, end=-1):
        assert self.doc_length >= self.test_num + self.train_num

        if end == -1:
            end = self.doc_length

        data = self.pos_doc_list[start:end] + self.neg_doc_list[start:end]
        data_labels = [1] * len(self.pos_doc_list[start:end]) + [0] * len(self.neg_doc_list[start:end])
        # data_labels = [1] * (end - start) + [0] * (end - start)
        data_combined = list(zip(data, data_labels))
        shuffle(data_combined)
        data[:], data_labels[:] = zip(*data_combined)

        return data, data_labels

    def get_train_corpus(self, num):
        self.train_num = num
        return self.get_corpus(end=num)

    def get_test_corpus(self, num):
        self.test_num = num
        return self.get_corpus(start=self.train_num, end=self.train_num + num)

class TwitterCorpus(Corpus):
    def __init__(self):
        Corpus.__init__(self, "data/tweets_rele.txt")

def get_keywords(keywordpath):
    root_path = os.path.dirname(os.path.abspath(__file__))
    keywordpath = os.path.normpath(os.path.join(root_path, keywordpath))

    # keyword_split = re.compile("\0")

    keywords_list = []
    with open(keywordpath, encoding="utf-8") as f:
        for line in f:
            # keywords_splits = keyword_split.split(line.strip())
            keyword = line.replace('\n', '')
            keywords_list.append(keyword)

        return keywords_list

if __name__ == "__main__":
    pass
