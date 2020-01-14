# -*- coding: utf-8 -*-
import os
import jsonlines
import json
import random

def judge(theme):
    Text = {"relevance":{"1":"\n请判断本推文是否与中国70周年国庆有关？1有关，2无关：", 
        "2": "输入不在允许范围内！请重新判断本推文是否与中国70周年国庆有关？1有关，2无关：", 
        "3": "\n输入非指定项！请重新判断本推文是否与中国70周年国庆有关？1有关，2无关："}, 
        "type": {"1": "本推文是简体还是繁体？1是简体，2是繁体：", 
        "2": "输入不在允许范围内！请重新判断本推文是简体还是繁体？1是简体，2是繁体：", 
        "3": "\n输入非指定项！请重新判断本推文是简体还是繁体？1是简体，2是繁体："}, 
        "sentiment": {"1": "请为本推文的情感态度打分，5为非常积极，4为积极，3为无明显感情，2为消极，1为非常消极：", 
        "2": "输入不在允许范围内！请重新为本推文的情感态度打分，5为非常积极，4为积极，3为无明显感情，2为消极，1为非常消极：",
        "3": "\n输入非指定项！请重新为本推文的情感态度打分，5为非常积极，4为积极，3为无明显感情，2为消极，1为非常消极："},
        "ScoringPersonNumber": {"1": "\n您好！请输入您的编号：",
        "2": "输入不在允许范围内！请重新输入：",
        "3": "\n输入非指定项！请重新输入："}}
    Range = {"relevance": ["1", "2"], "type": ["1", "2"], "sentiment": ["5", "4", "3", "2", "1"], "ScoringPersonNumber": ["1", "2", "3", "4"]}
    try:
        judge = input(Text[theme]["1"])
        while judge not in Range[theme]:
            judge = input(Text[theme]["2"])
    except:
        judge = input(Text[theme]["3"])
        while judge not in Range[theme]:
            judge = input(Text[theme]["2"])
    return judge

file_path_en = os.getcwd()+'/labeled_data/en.jsonl'
file_path_zh = os.getcwd()+'/labeled_data/zh.jsonl'
file_path_num = os.getcwd()+'/labeled_data/num.jsonl'

ScoringPersonNumber = judge("ScoringPersonNumber")

with open (file_path_num, "r") as file:
    for info in jsonlines.Reader(file):
        num_to_label = info['en']
        num_to_label_zh = info['zh']

print ('\n-------以下为英文推特情感态度打分，共{}条-------\n'.format(num_to_label))

with open (file_path_en, "r") as f:
    # print (file_en)
    count = 1
    for tweets in jsonlines.Reader(f):
        print ("No.{}\n".format(count))
        print (tweets["text"])
        rele = int(judge("relevance"))
        # tweets['rele'] = rele
        if rele == 1:
            sentiment = int(judge("sentiment")) - 3
            labeled_tweet = {'created_at': '{}'.format(tweets["created_at"]), 'text': '{}'.format(tweets["text"]), 
                            'rele': '{}'.format(rele), 'sentiment': '{}'.format(sentiment)}
            # labeled_tweet = {'created_at': '{}'.format(tweets["created_at"]), 'text': '{}'.format(tweets["text"]), 'sentiment': '{}'.format(sentiment)}
            # with open (target_path_en, "a") as file:
            #     file.write(json.dumps(labeled_tweet)+'\n')
        else:
            labeled_tweet = {'created_at': '{}'.format(tweets["created_at"]), 'text': '{}'.format(tweets["text"]), 
                            'rele': '{}'.format(rele), 'sentiment': ''}
        with open ('labeled_data/en_{}.jsonl'.format(ScoringPersonNumber), "a") as file:
            file.write(json.dumps(labeled_tweet)+'\n')
        count += 1
        print ('\n****************************下一个****************************\n')

print ('\n-------接下来为中文推特情感态度打分，包括简体和繁体，共{}条-------\n'.format(num_to_label_zh))

with open (file_path_zh, "r") as f:
    # print (file_zh_cn)
    count = 1
    for tweets in jsonlines.Reader(f):
        print ("No.{}\n".format(count))
        print (tweets["text"])
        rele = int(judge("relevance"))
        ctype = judge("type")
        # tweets['rele'] = rele
        # tweets['type{}'.format(ScoringPersonNumber)] = ctype
        if rele == 1:
            sentiment = int(judge("sentiment")) - 3
            labeled_tweet = {'created_at': '{}'.format(tweets["created_at"]), 'text': '{}'.format(tweets["text"]), 
                            'rele': '{}'.format(rele), 'sentiment': '{}'.format(sentiment), 'type': '{}'.format(ctype)}
            # tweets['sentiment{}'.format(ScoringPersonNumber)] = sentiment
            # labeled_tweet = {'created_at': '{}'.format(tweets["created_at"]), 'text': '{}'.format(tweets["text"]), 'sentiment': '{}'.format(sentiment)}
            # with open ('labeled_data/zh{}.jsonl'.format(ctype), "a") as file:
            #     file.write(json.dumps(labeled_tweet)+'\n')
        else:
            labeled_tweet = {'created_at': '{}'.format(tweets["created_at"]), 'text': '{}'.format(tweets["text"]), 
                            'rele': '{}'.format(rele), 'sentiment': '', 'type': '{}'.format(ctype)}
        with open ('labeled_data/zh_{}.jsonl'.format(ScoringPersonNumber), "a") as file:
            file.write(json.dumps(labeled_tweet)+'\n')
        count += 1
        print ('\n****************************下一个****************************\n')

print ('\n-------您已完成打分，谢谢！-------\n')