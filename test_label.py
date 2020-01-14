import os
import jsonlines
import numpy as np

basic_path = os.getcwd()
file_en_1 = basic_path + "/labeled_data/en_1.jsonl"
file_en_2 = basic_path + "/labeled_data/en_2.jsonl"
file_en_3 = basic_path + "/labeled_data/en_3.jsonl"
file_en_4 = basic_path + "/labeled_data/en_4.jsonl"
file_zh_1 = basic_path + "/labeled_data/zh_1.jsonl"
file_zh_2 = basic_path + "/labeled_data/zh_2.jsonl"
file_zh_3 = basic_path + "/labeled_data/zh_3.jsonl"
file_zh_4 = basic_path + "/labeled_data/zh_4.jsonl"
file_final = basic_path + '/labeled_data/test_label_result.txt'

tweets_en = 1000
tweets_zh = 999
result_rele_en = [0, 0, 0]                  # 4:0, 3:1, 2:2
result_sentiment_en = [0, 0, 0, 0, 0]       # 4:0, 3:1, 2:2, 2:1:1, 1:1:1:1
result_sentiment3_en = [0, 0, 0]            # 3:0, 2:1, 1:1:1
result_rele_zh = [0, 0, 0]
result_type_zh = [0, 0, 0]
result_sentiment_zh = [0, 0, 0, 0, 0]
result_sentiment3_zh = [0, 0, 0]
isTaiwan_rele_en = 0
isTaiwan_sentiment_en = 0
isTaiwan_sentiment3_en = 0
isTaiwan_rele_zh = 0
isTaiwan_sentiment_zh = 0
isTaiwan_sentiment3_zh = 0
isTaiwan_type_zh = 0

result_sentiment_p0n_en = [0, 0, 0, 0]      # 4:0, 3:1, 2:2, 2:1:1
result_sentiment3_p0n_en = [0, 0, 0]        # 3:0, 2:1, 1:1:1
result_sentiment_p0n_zh = [0, 0, 0, 0]
result_sentiment3_p0n_zh = [0, 0, 0]
isTaiwan_sentiment_p0n_en = 0
isTaiwan_sentiment3_p0n_en = 0
isTaiwan_sentiment_p0n_zh = 0
isTaiwan_sentiment3_p0n_zh = 0

def findratio(num):
    if num[0] == num[3]:
        return 0
    elif num[0] == num[2] or num[1] == num[3]:
        return 1
    elif num[0] == num[1] and num[2] == num[3]:
        return 2
    elif num[0] == num[1] and num[2] != num[3]:
        return 3
    elif num[0] != num[1] and num[2] == num[3]:
        return 3
    elif num[0] != num[1] and num[1] == num[2] and num[2] != num[3]:
        return 3
    elif num[0] != num[1] and num[1] != num[2] and num[2] != num[3]:
        return 4
    else:
        print (num)
        raise ValueError('没考虑到！')

def findratio_p0n(num):
    if num[0] == num[3]:
        return 0
    elif num[0] == num[2] or num[1] == num[3]:
        return 1
    elif num[0] == num[1] and num[2] == num[3]:
        return 2
    elif num[0] == num[1] and num[2] != num[3]:
        return 3
    elif num[0] != num[1] and num[2] == num[3]:
        return 3
    elif num[0] != num[1] and num[1] == num[2] and num[2] != num[3]:
        return 3
    else:
        print (num)
        raise ValueError('没考虑到！')

def findratio3(num):                   # 本函数无论是否将+2，-2合并为+时都可使用
    if num[0] == num[2]:
        return 0
    elif num[0] == num[1] or num[1] == num[2]:
        return 1
    elif num[0] != num[1] and num[1] != num[2]:
        return 2
    else:
        raise ValueError('没考虑到！')

def isTaiwan(num):
    if num[1] != num[0] and num[0] == num[2] == num[3]:
        return 1
    else:
        return 0

def isTaiwan3(num, num_Taiwan, res_sent):
    if res_sent == 0 or res_sent == 2:
        return 0
    elif res_sent == 1:
        index = [i for i in range(len(num)) if num[i] == num_Taiwan]
        if len(index) == 1:
            return 1
        elif len(index) == 2:
            return 0
        else:
            print (num, num_Taiwan, index)
            raise ValueError('还是不对！')
    else:
        raise ValueError('类别不对！')

def modify(num):
    res = []
    for i in range(len(num)):
        res.append(np.sign(num[i]))
    return res

def test(file_1, file_2, file_3, file_4, result_rele, result_sentiment, result_sentiment_p0n, result_sentiment3, result_sentiment3_p0n, isTaiwan_rele, isTaiwan_sentiment,
        isTaiwan_sentiment_p0n, isTaiwan_sentiment3, isTaiwan_sentiment3_p0n, total_num, result_type = [], isTaiwan_type = 0):
    count = 0
    Taiwan_count = 0
    with open(file_1, 'r') as f1:
        with open(file_2, 'r') as f2:
            with open(file_3, 'r') as f3:
                with open(file_4, 'r') as f4:
                    for t1 in jsonlines.Reader(f1):
                        for t2 in jsonlines.Reader(f2):
                            if t1['created_at'] == t2['created_at'] and t1['text'] == t2['text']:
                                for t3 in jsonlines.Reader(f3):
                                    if t1['created_at'] == t3['created_at'] and t1['text'] == t3['text']:
                                        for t4 in jsonlines.Reader(f4):
                                            if t1['created_at'] == t4['created_at'] and t1['text'] == t4['text']:
                                                count += 1
                                                print (count)
                                                num_rele = [int(t1['rele']), int(t2['rele']), int(t3['rele']), int(t4['rele'])]
                                                isTaiwan_rele += isTaiwan(num_rele)
                                                num_rele.sort()
                                                res_rele = findratio(num_rele)
                                                result_rele[res_rele] += 1
                                                if result_type != []:
                                                    num_type = [int(t1['type']), int(t2['type']), int(t3['type']), int(t4['type'])]
                                                    isTaiwan_type += isTaiwan(num_type)
                                                    num_type.sort()
                                                    res_type = findratio(num_type)
                                                    result_type[res_type] += 1
                                                if res_rele == 0 and t1['rele'] == "1":
                                                    num_sent = [int(t1['sentiment']), int(t2['sentiment']), int(t3['sentiment']), int(t4['sentiment'])]
                                                    num_sent_p0n = modify(num_sent)
                                                    isTaiwan_sentiment += isTaiwan(num_sent)
                                                    isTaiwan_sentiment_p0n += isTaiwan(num_sent_p0n)
                                                    num_sent.sort()
                                                    res_sent = findratio(num_sent)
                                                    result_sentiment[res_sent] += 1
                                                    num_sent_p0n.sort()
                                                    res_sent_p0n = findratio_p0n(num_sent_p0n)
                                                    result_sentiment_p0n[res_sent_p0n] += 1
                                                elif res_rele == 1 and num_rele[1] == num_rele[2] == 1:   # 如果是3:1，而且3的一方是相关
                                                    num_sent = []
                                                    if t1['sentiment'] != "":
                                                        num_sent.append(int(t1['sentiment']))
                                                    if t2['sentiment'] != "":
                                                        isCalTaiwan = True
                                                        num_Taiwan = int(t2['sentiment'])
                                                        num_sent.append(num_Taiwan)
                                                    else:
                                                        isCalTaiwan = False
                                                    if t3['sentiment'] != "":
                                                        num_sent.append(int(t3['sentiment']))
                                                    if t4['sentiment'] != "":
                                                        num_sent.append(int(t4['sentiment']))
                                                    try:
                                                        assert len(num_sent) == 3
                                                    except:
                                                        print (t1['sentiment'], t2['sentiment'], t3['sentiment'], t4['sentiment'], num_sent)
                                                        raise ValueError('不是三个！')
                                                    num_sent_p0n = modify(num_sent)
                                                    num_sent.sort()
                                                    res_sent = findratio3(num_sent)
                                                    result_sentiment3[res_sent] += 1
                                                    num_sent_p0n.sort()
                                                    res_sent_p0n = findratio3(num_sent_p0n)
                                                    result_sentiment3_p0n[res_sent_p0n] += 1
                                                    if isCalTaiwan == True:
                                                        # if res_sent == 1:
                                                        #     Taiwan_count___ += 1     # 非pos、0、neg的情况，暂时没用到
                                                        if res_sent_p0n == 1:
                                                            Taiwan_count += 1
                                                        isTaiwan_sentiment3 += isTaiwan3(num_sent, num_Taiwan, res_sent)
                                                        isTaiwan_sentiment3_p0n += isTaiwan3(num_sent_p0n, np.sign(num_Taiwan), res_sent_p0n)
                                                break
                                        break
                                break
    assert count == total_num
    return isTaiwan_rele, isTaiwan_sentiment, isTaiwan_sentiment_p0n, isTaiwan_sentiment3, isTaiwan_sentiment3_p0n, isTaiwan_type, Taiwan_count

isTaiwan_rele_en, isTaiwan_sentiment_en, isTaiwan_sentiment_p0n_en, isTaiwan_sentiment3_en, isTaiwan_sentiment3_p0n_en, no_matter, Taiwan_count_en = \
    test(file_en_1, file_en_2, file_en_3, file_en_4, result_rele_en, result_sentiment_en, result_sentiment_p0n_en, result_sentiment3_en, result_sentiment3_p0n_en, 
        isTaiwan_rele_en, isTaiwan_sentiment_en, isTaiwan_sentiment_p0n_en, isTaiwan_sentiment3_en, isTaiwan_sentiment3_p0n_en, tweets_en)
isTaiwan_rele_zh, isTaiwan_sentiment_zh, isTaiwan_sentiment_p0n_zh, isTaiwan_sentiment3_zh, isTaiwan_sentiment3_p0n_zh, isTaiwan_type_zh, Taiwan_count_zh = \
    test(file_zh_1, file_zh_2, file_zh_3, file_zh_4, result_rele_zh, result_sentiment_zh, result_sentiment_p0n_zh, result_sentiment3_zh, result_sentiment3_p0n_zh, 
        isTaiwan_rele_zh, isTaiwan_sentiment_zh, isTaiwan_sentiment_p0n_zh, isTaiwan_sentiment3_zh, isTaiwan_sentiment3_p0n_zh, tweets_zh, result_type_zh, isTaiwan_type_zh)

assert sum(result_rele_en) == tweets_en
assert sum(result_rele_zh) == tweets_zh
assert sum(result_type_zh) == tweets_zh

with open (file_final, 'w') as f:
    f.write('result_rele_en = ' + str(result_rele_en) + '\n')
    f.write('result_sentiment_en = ' + str(result_sentiment_en) + '\n')
    f.write('result_sentiment3_en = ' + str(result_sentiment3_en) + '\n')
    f.write('result_sentiment_p0n_en = ' + str(result_sentiment_p0n_en) + '\n')
    f.write('result_sentiment3_p0n_en = ' + str(result_sentiment3_p0n_en) + '\n')
    f.write('result_rele_zh = ' + str(result_rele_zh) + '\n')
    f.write('result_type_zh = ' + str(result_type_zh) + '\n')
    f.write('result_sentiment_zh = ' + str(result_sentiment_zh) + '\n')
    f.write('result_sentiment3_zh = ' + str(result_sentiment3_zh) + '\n')
    f.write('result_sentiment_p0n_zh = ' + str(result_sentiment_p0n_zh) + '\n')
    f.write('result_sentiment3_p0n_zh = ' + str(result_sentiment3_p0n_zh) + '\n')
    f.write('isTaiwan_rele_en = ' + str(isTaiwan_rele_en) + '\n')
    f.write('isTaiwan_sentiment_en = ' + str(isTaiwan_sentiment_en) + '\n')
    f.write('isTaiwan_sentiment3_en = ' + str(isTaiwan_sentiment3_en) +'\n') # + ', labeler 2 participated ' + str(Taiwan_count___en) + ' times in total.' + '\n')
    f.write('isTaiwan_sentiment_p0n_en = ' + str(isTaiwan_sentiment_p0n_en) + '\n')
    f.write('isTaiwan_sentiment3_p0n_en = ' + str(isTaiwan_sentiment3_p0n_en) + ', labeler 2 participated ' + str(Taiwan_count_en) + ' times in total.' + '\n')
    f.write('isTaiwan_rele_zh = ' + str(isTaiwan_rele_zh) + '\n')
    f.write('isTaiwan_sentiment_zh = ' + str(isTaiwan_sentiment_zh) + '\n')
    f.write('isTaiwan_sentiment3_zh = ' + str(isTaiwan_sentiment3_zh) +'\n') # + ', labeler 2 participated ' + str(Taiwan_count___zh) + ' times in total.' + '\n')
    f.write('isTaiwan_type_zh = ' + str(isTaiwan_type_zh) + '\n')
    f.write('isTaiwan_sentiment_p0n_zh = ' + str(isTaiwan_sentiment_p0n_zh) + '\n')
    f.write('isTaiwan_sentiment3_p0n_zh = ' + str(isTaiwan_sentiment3_p0n_zh) + ', labeler 2 participated ' + str(Taiwan_count_zh) + ' times in total.' + '\n')