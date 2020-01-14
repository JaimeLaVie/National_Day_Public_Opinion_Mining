# -*- coding: utf-8 -*-
import os
import jsonlines
import json
import random

def line_num(file):
    num = 0
    with open (file, "r") as f:
        for line in f:
            num += 1
    return num

file_en = os.getcwd()+'/preprocessing_0929_1003/en.jsonl'
file_zh_cn = os.getcwd()+'/preprocessing_0929_1003/zh-cn.jsonl'
file_zh_tw = os.getcwd()+'/preprocessing_0929_1003/zh-tw.jsonl'
files_zh = [file_zh_cn, file_zh_tw]
target_path_en = os.getcwd()+'/labeled_data/en.jsonl'
target_path_zh = os.getcwd()+'/labeled_data/zh.jsonl'
target_path_num = os.getcwd()+'/labeled_data/num.jsonl'

num_en = line_num(file_en)
num_zh_cn = line_num(file_zh_cn)
num_zh_tw = line_num(file_zh_tw)
num_zh = num_zh_cn + num_zh_tw
num_total = num_en + num_zh
num_to_label = 1000
num_to_label_cn = num_to_label * num_zh_cn // num_zh
num_to_label_tw = num_to_label * num_zh_tw // num_zh
num_to_label_zh = num_to_label_cn + num_to_label_tw
# print (num_en, num_zh_cn, num_zh_tw, num_to_label_cn, num_to_label_tw)

with open (target_path_num, "w") as file:
    num = {'en': num_to_label, 'zh': num_to_label_zh}
    file.write(json.dumps(num))

with open (file_en, "r") as f:
    # print (file_en)
    index = random.sample(range(1, num_en), num_to_label)
    count = 1
    for tweets in jsonlines.Reader(f):
        if count in index:
            print (tweets["text"])
            labeled_tweet = {'created_at': '{}'.format(tweets["created_at"]), 'text': '{}'.format(tweets["text"])}
                            # 'rele1': '','rele2': '', 'rele3': '', 'sentiment1': '', 'sentiment2': '', 'sentiment3': '', 'OverallSentiment': ''}
            with open (target_path_en, "a") as file:
                file.write(json.dumps(labeled_tweet)+'\n')
        count += 1

with open (file_zh_cn, "r") as f:
    # print (file_zh_cn)
    index = random.sample(range(1, num_zh_cn), num_to_label_cn)
    count = 1
    for tweets in jsonlines.Reader(f):
        if count in index:
            print (tweets["text"])
            labeled_tweet = {'created_at': '{}'.format(tweets["created_at"]), 'text': '{}'.format(tweets["text"])}
                            # 'rele1': '','rele2': '', 'rele3': '', 'sentiment1': '', 'sentiment2': '', 'sentiment3': '', 'OverallSentiment': '', 
                            # 'type1': '', 'type2': '', 'type3': ''}
            with open (target_path_zh, "a") as file:
                file.write(json.dumps(labeled_tweet)+'\n')
        count += 1

with open (file_zh_tw, "r") as f:
    # print (file_zh_tw)
    index = random.sample(range(1, num_zh_tw), num_to_label_tw)
    count = 1
    for tweets in jsonlines.Reader(f):
        if count in index:
            print (tweets["text"])
            labeled_tweet = {'created_at': '{}'.format(tweets["created_at"]), 'text': '{}'.format(tweets["text"])}
                            # 'rele1': '','rele2': '', 'rele3': '', 'sentiment1': '', 'sentiment2': '', 'sentiment3': '', 'OverallSentiment': '', 
                            # 'type1': '', 'type2': '', 'type3': ''}
            with open (target_path_zh, "a") as file:
                file.write(json.dumps(labeled_tweet)+'\n')
        count += 1
