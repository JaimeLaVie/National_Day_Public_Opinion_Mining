import os
import random
import jsonlines
import json

# 英文数据量过大，故随机抽取2000条地名进行标注和可视化

basic_path = os.getcwd()
file_path_pos_en = basic_path + "/result/pos_location_en.jsonl"
file_path_neg_en = basic_path + "/result/neg_location_en.jsonl"
file_path_target_pos_en = basic_path + "/locations/pos_selected_location_en.jsonl"
file_path_target_neg_en = basic_path + "/locations/neg_selected_location_en.jsonl"

try:
    os.remove(file_path_target_pos_en)
    os.remove(file_path_target_neg_en)
except:
    print ('Delete failed!')

n_sample = 2000
n_p = 0
n_n = 0

with open (file_path_pos_en, 'r') as fp:
    for line in jsonlines.Reader(fp):
        pos = line
        print('pos')
        for items in line:
            n_p += 1

with open (file_path_neg_en, 'r') as fn:
    for line in jsonlines.Reader(fn):
        neg = line
        print('neg')
        for items in line:
            n_n += 1

print (n_p, n_n)
n_sp = round(n_sample * n_p / (n_p + n_n))
n_sn = round(n_sample * n_n / (n_p + n_n))

index_p = random.sample(range(0, n_p), n_sp)
index_n = random.sample(range(0, n_n), n_sn)

count_p = 0
count_itemp = 0
location_p = {}
for itemp in pos:
    if count_p in index_p:
        location_p[itemp] = pos[itemp]
        count_itemp += 1
    count_p += 1

print (count_itemp)
with open(file_path_target_pos_en, 'a') as fo:
    fo.write(json.dumps(location_p))

count_n = 0
count_itemn = 0
location_n = {}
for itemn in neg:
    if count_n in index_n:
        location_n[itemn] = neg[itemn]
        count_itemn += 1
    count_n += 1

print (count_itemn)
with open(file_path_target_neg_en, 'a') as fo:
    fo.write(json.dumps(location_n))
