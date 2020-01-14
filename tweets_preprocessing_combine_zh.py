# -*- coding: utf-8 -*-
import os
import jsonlines
# import csv
import json

# file1 = os.getcwd()+'/preprocessing_0929_1003/zh-cn.jsonl'
# file2 = os.getcwd()+'/preprocessing_0929_1003/zh-tw.jsonl'
# file_target = os.getcwd()+'/preprocessing_0929_1003/zh.jsonl'
file1 = os.getcwd()+'/preprocessing/zh-cn.jsonl'
file2 = os.getcwd()+'/preprocessing/zh-tw.jsonl'
file_target = os.getcwd()+'/preprocessing/zh.jsonl'

with open (file1, 'r') as f1:
    for tweets in jsonlines.Reader(f1):
        with open (file_target, "a") as ft:
            ft.write(json.dumps(tweets)+'\n')

with open (file2, 'r') as f2:
    for tweets in jsonlines.Reader(f2):
        with open (file_target, "a") as ft:
            ft.write(json.dumps(tweets)+'\n')
