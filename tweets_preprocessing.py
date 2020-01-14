# -*- coding: utf-8 -*-
import os
import jsonlines
# import csv
import json
from langdetect import detect

def TweetsClassifier(InputFile):
    print (InputFile)
    with open (InputFile, "r") as f:
        for tweets in jsonlines.Reader(f):
            # print(tweets["created_at"], tweets["text"])
            # stu = [tweets["created_at"], tweets["text"]]
            # out = open('preprocessing/preprocessing.csv','a', newline = '', encoding='utf-8')
            # csv_write = csv.writer(out, dialect='excel')
            # csv_write.writerow(stu)
            try:          #防止出现类似{"limit":{"track":8,"timestamp_ms":"1569986100469"}}的一行使得程序执行报错
                # tweet = {'created_at': '{}'.format(tweets["created_at"]), 'text': '{}'.format(tweets["text"])}
                tweet = tweets
                try:
                    # print (detect(tweets['text']))
                    lang = detect(tweets['text'])
                    # isExist = os.path.exists('{}/{}'.format(targetdir, lang))
                    # if not isExist:
                    #     os.makedirs('{}/{}'.format(targetdir, lang))
                    # with open ('{}/{}/{}.jsonl'.format(targetdir, lang, FileName), "a") as file:
                    #     file.write(json.dumps(tweet)+'\n')
                    with open ('{}/{}.jsonl'.format(targetdir, lang), "a") as file:
                        file.write(json.dumps(tweet)+'\n')
                except:
                    # print ("****************************NOT LANGUAGE****************************")
                    with open ('{}/preprocessing_not_language.jsonl'.format(targetdir), "a") as file:
                        file.write(json.dumps(tweet)+'\n')
            except:
                pass

def TweetsClassifier_del_mult(InputFile):
    print (InputFile)
    with open (InputFile, "r") as f:
        id_last = 0
        id_now = 0
        for tweets in jsonlines.Reader(f):
            id_now = tweets['id']
            if id_now == id_last:
                continue
            else:
                id_last = id_now
                try:          #防止出现类似{"limit":{"track":8,"timestamp_ms":"1569986100469"}}的一行使得程序执行报错
                    tweet = tweets
                    try:
                        # print (detect(tweets['text']))
                        lang = detect(tweets['text'])
                        with open ('{}/{}.jsonl'.format(targetdir, lang), "a") as file:
                            file.write(json.dumps(tweet)+'\n')
                    except:
                        with open ('{}/preprocessing_not_language.jsonl'.format(targetdir), "a") as file:
                            file.write(json.dumps(tweet)+'\n')
                except:
                    pass

filedir1 = os.getcwd()+'/data_0929_1003'
filenames1=os.listdir(filedir1)
filedir2 = os.getcwd()+'/data_1005_1008'
filenames2=os.listdir(filedir2)
targetdir = os.getcwd()+'/preprocessing'

for filename in filenames1:
    filepath = filedir1+'/'+filename
    # print (filepath)
    # targetpath = targetdir+'/'+
    TweetsClassifier(filepath)

for filename in filenames2:
    filepath = filedir2+'/'+filename
    # print (filepath)
    # targetpath = targetdir+'/'+
    TweetsClassifier_del_mult(filepath)
