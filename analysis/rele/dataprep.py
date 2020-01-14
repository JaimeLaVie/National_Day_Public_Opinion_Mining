import os
import jsonlines
import thulac
import re

'''
数据处理，包括去除网页链接、分词、用空格替代换行，并将rele标签与推文合并写入到文件中。
'''

file_path_zh = '../../labeled_data/zh_final.jsonl'
file_path_target = 'data/tweets_rele.txt'
thuseg = thulac.thulac(seg_only=True, filt = False)

try:
    os.remove(file_path_target)
except:
    print ('failed')
    pass

def delurl(text, url):
    for i in range (len(url)):
        text = text.replace(str(url[i]), '')
    return text

with open (file_path_zh, "r") as f:
    for tweet in jsonlines.Reader(f):
        rele = tweet['rele']
        text = tweet['text']
        url = re.findall(r'http[a-zA-Z0-9\.\?\/\&\=\:\^\%\$\#\!]*', text)
        text = delurl(text, url)
        text = thuseg.cut(text, text=True)
        text = text.replace("\n", "\0")
        text = rele + '\0' + text + '\n'
        # print (text)
        with open(file_path_target,"a", encoding = 'UTF-8') as f:
            f.write(text)
