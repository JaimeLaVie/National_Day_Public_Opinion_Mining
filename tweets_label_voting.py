# -*- coding: utf-8 -*-
import os
import jsonlines
import json
import numpy as np
import random

file_1_en = os.getcwd()+'/labeled_data/en_1.jsonl'
file_1_zh = os.getcwd()+'/labeled_data/zh_1.jsonl'
file_2_en = os.getcwd()+'/labeled_data/en_2.jsonl'
file_2_zh = os.getcwd()+'/labeled_data/zh_2.jsonl'
file_3_en = os.getcwd()+'/labeled_data/en_3.jsonl'
file_3_zh = os.getcwd()+'/labeled_data/zh_3.jsonl'
file_4_en = os.getcwd()+'/labeled_data/en_4.jsonl'
file_4_zh = os.getcwd()+'/labeled_data/zh_4.jsonl'
file_final_en = os.getcwd()+'/labeled_data/en_final.jsonl'
file_final_zh = os.getcwd()+'/labeled_data/zh_final.jsonl'

try:
    os.remove(file_final_en)
except:
    pass

try:
    os.remove(file_final_zh)
except:
    pass

def majority_element(nums: list) -> int:
    num_hash = {}
    for i in nums:
        if i in num_hash:
            num_hash[i] += 1
        else:
            num_hash[i] = 1
    sorted_list = sorted(num_hash.items(), key=lambda x: x[1], reverse=True)
    # print (sorted_list)
    try:
        if sorted_list[0][1] == sorted_list[3][1]:
            r = random.randint(0,3)
            if r == 0:
                output = sorted_list[0][0]
            elif r == 1:
                output = sorted_list[1][0]
            elif r == 2:
                output = sorted_list[2][0]
            else:
                output = sorted_list[3][0]
    except:
        try:
            if sorted_list[0][1] == sorted_list[1][1]:
                r = random.randint(0,1)
                if r == 0:
                    output = sorted_list[0][0]
                else:
                    output = sorted_list[1][0]
            else:
                output = sorted_list[0][0]
        except:
            output = sorted_list[0][0]
    return output

def vote(d1, d2, d3, d4):
    nums = []
    if d1 is not '':
        nums.append(int(d1))
    if d2 is not '':
        nums.append(int(d2))
    if d3 is not '':
        nums.append(int(d3))
    if d4 is not '':
        nums.append(int(d4))
    return str(majority_element(nums))

count = 0
with open (file_final_en, 'a') as target:
    with open (file_1_en, 'r') as f1:
        for t1 in jsonlines.Reader(f1):
            # print (t1)
            with open (file_2_en, 'r') as f2:
                for t2 in jsonlines.Reader(f2):
                    # print (t2)
                    if t1['created_at'] == t2['created_at'] and t1['text'] == t2['text']:
                        with open (file_3_en, 'r') as f3:
                            for t3 in jsonlines.Reader(f3):
                                if t1['created_at'] == t3['created_at'] and t1['text'] == t3['text']:
                                    with open (file_4_en, 'r') as f4:
                                        for t4 in jsonlines.Reader(f4):
                                            if t1['created_at'] == t4['created_at'] and t1['text'] == t4['text']:
                                                count += 1
                                                print (count)
                                                target_text = {}
                                                target_text['created_at'] = t1['created_at']
                                                target_text['text'] = t1['text']
                                                target_text['rele'] = vote(t1['rele'], t2['rele'], t3['rele'], t4['rele'])
                                                if target_text['rele'] == "1":
                                                    target_text['sentiment'] = vote(t1['sentiment'], t2['sentiment'], t3['sentiment'], t4['sentiment'])
                                                else:
                                                    target_text['sentiment'] = ''
                                                target.write(json.dumps(target_text) + '\n')
                                                break
                                    break
                        break
assert count == 1000

count = 0
with open (file_final_zh, 'a') as target:
    with open (file_1_zh, 'r') as f1:
        for t1 in jsonlines.Reader(f1):
            # print (t1)
            with open (file_2_zh, 'r') as f2:
                for t2 in jsonlines.Reader(f2):
                    # print (t2)
                    if t1['created_at'] == t2['created_at'] and t1['text'] == t2['text']:
                        with open (file_3_zh, 'r') as f3:
                            for t3 in jsonlines.Reader(f3):
                                if t1['created_at'] == t3['created_at'] and t1['text'] == t3['text']:
                                    with open (file_4_zh, 'r') as f4:
                                        for t4 in jsonlines.Reader(f4):
                                            if t1['created_at'] == t4['created_at'] and t1['text'] == t4['text']:
                                                count += 1
                                                print (count)
                                                target_text = {}
                                                target_text['created_at'] = t1['created_at']
                                                target_text['text'] = t1['text']
                                                target_text['rele'] = vote(t1['rele'], t2['rele'], t3['rele'], t4['rele'])
                                                if target_text['rele'] == "1":
                                                    target_text['sentiment'] = vote(t1['sentiment'], t2['sentiment'], t3['sentiment'], t4['sentiment'])
                                                else:
                                                    target_text['sentiment'] = ''
                                                target_text['type'] = vote(t1['type'], t2['type'], t3['type'], t4['type'])
                                                target.write(json.dumps(target_text) + '\n')
                                                break
                                    break
                        break
assert count == 999