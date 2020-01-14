import os
import shutil
import re
import jsonlines
import json
import random
from rele_en import Classify as Classify_rele_en
from sentiment_en import Classify as Classify_sentiment_en
from sentiment_posneg_en import Classify as Classify_sentiment_posneg_en
import thulac
from rele import Classify as Classify_rele
from type import Classify as Classify_type
from sentiment import Classify as Classify_sentiment
from sentiment_posneg import Classify as Classify_sentiment_posneg
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
# import matplotlib.dates as mdates
# from datetime import datetime

basic_path = os.getcwd()
time_29 = ['Sep-29 10h', 'Sep-29 11h', 'Sep-29 12h', 'Sep-29 13h', 'Sep-29 14h', 'Sep-29 15h', 'Sep-29 16h', 'Sep-29 17h', 'Sep-29 18h', 
        'Sep-29 19h', 'Sep-29 20h']
time_30_03 = ['Sep-30 8h', 'Sep-30 9h', 'Sep-30 10h', 'Sep-30 11h', 'Sep-30 12h', 'Sep-30 13h', 'Sep-30 14h', 'Sep-30 15h', 
        'Sep-30 16h', 'Sep-30 17h', 'Sep-30 18h', 'Sep-30 19h', 'Sep-30 20h', 'Sep-30 21h', 'Sep-30 22h', 'Sep-30 23h', 'Oct-01 0h', 'Oct-01 1h', 
        'Oct-01 2h', 'Oct-01 3h', 'Oct-01 4h', 'Oct-01 5h', 'Oct-01 6h', 'Oct-01 7h', 'Oct-01 8h', 'Oct-01 9h', 'Oct-01 10h', 'Oct-01 11h', 
        'Oct-01 12h', 'Oct-01 13h', 'Oct-01 14h', 'Oct-01 15h', 'Oct-01 16h', 'Oct-01 17h', 'Oct-01 18h', 'Oct-01 19h', 'Oct-01 20h', 'Oct-01 21h', 
        'Oct-01 22h', 'Oct-01 23h', 'Oct-02 0h', 'Oct-02 1h', 'Oct-02 2h', 'Oct-02 3h', 'Oct-02 4h', 'Oct-02 5h', 'Oct-02 6h', 'Oct-02 7h', 
        'Oct-02 8h', 'Oct-02 9h', 'Oct-02 10h', 'Oct-02 11h', 'Oct-02 12h', 'Oct-02 13h', 'Oct-02 14h', 'Oct-02 15h', 'Oct-02 16h', 'Oct-02 17h', 
        'Oct-02 18h', 'Oct-02 19h', 'Oct-02 20h', 'Oct-02 21h', 'Oct-02 22h', 'Oct-02 23h', 'Oct-03 0h', 'Oct-03 1h', 'Oct-03 2h', 'Oct-03 3h', 
        'Oct-03 4h', 'Oct-03 5h', 'Oct-03 6h', 'Oct-03 7h', 'Oct-03 8h', 'Oct-03 9h', 'Oct-03 10h']
time_05_08 = ['Oct-05 11h', 'Oct-05 12h', 'Oct-05 13h', 'Oct-05 14h', 'Oct-05 15h', 'Oct-05 16h', 'Oct-05 17h', 'Oct-05 18h', 'Oct-05 19h', 
        'Oct-05 20h', 'Oct-05 21h', 'Oct-05 22h', 'Oct-05 23h', 'Oct-06 0h', 'Oct-06 1h', 'Oct-06 2h', 'Oct-06 3h', 'Oct-06 4h', 'Oct-06 5h', 
        'Oct-06 6h', 'Oct-06 7h', 'Oct-06 8h', 'Oct-06 9h', 'Oct-06 10h', 'Oct-06 11h', 'Oct-06 12h', 'Oct-06 13h', 'Oct-06 14h', 'Oct-06 15h', 
        'Oct-06 16h', 'Oct-06 17h', 'Oct-06 18h', 'Oct-06 19h', 'Oct-06 20h', 'Oct-06 21h', 'Oct-06 22h', 'Oct-06 23h', 'Oct-07 0h', 'Oct-07 1h', 
        'Oct-07 2h', 'Oct-07 3h', 'Oct-07 4h', 'Oct-07 5h', 'Oct-07 6h', 'Oct-07 7h', 'Oct-07 8h', 'Oct-07 9h', 'Oct-07 10h', 'Oct-07 11h', 
        'Oct-07 12h', 'Oct-07 13h', 'Oct-07 14h', 'Oct-07 15h', 'Oct-07 16h', 'Oct-07 17h', 'Oct-07 18h', 'Oct-07 19h', 'Oct-07 20h', 'Oct-07 21h', 
        'Oct-07 22h', 'Oct-07 23h', 'Oct-08 0h', 'Oct-08 1h', 'Oct-08 2h', 'Oct-08 3h', 'Oct-08 4h', 'Oct-08 5h', 'Oct-08 6h', 'Oct-08 7h', 
        'Oct-08 8h', 'Oct-08 9h', 'Oct-08 10h', 'Oct-08 11h', 'Oct-08 12h', 'Oct-08 13h', 'Oct-08 14h', 'Oct-08 15h', 'Oct-08 16h']
all_time = time_29 + time_30_03 + time_05_08

mode = 'all'  # 'test_on_2000'

def process_path(path):
    if os.path.exists(path):
        shutil.rmtree(path,True)
        print ('{} deleted'.format(path))
    os.mkdir(path)

if mode == 'test_on_2000':
    file_path_en = basic_path + "/../labeled_data/en_final.jsonl"
    file_path_zh = basic_path + "/../labeled_data/zh_final.jsonl"
    file_result = basic_path + "/result_on_labeled_data"
    process_path(file_result)
    scale_number_en = (0, 43)
    scale_number_zh = (0, 55)
    scale_number_zhs = (0, 45)
    scale_number_zht = (0, 8)
    scale_sentiment_en = (-35, 5)
    scale_sentiment_zh = (-10, 25)
    scale_sentiment_zhs = (-5, 20)
    scale_sentiment_zht = (-5, 5)
    scale_weighted_sentiment_en = (-105, 15)
    scale_weighted_sentiment_zh = (-30, 75)
    scale_weighted_sentiment_zhs = (-15, 60)
    scale_weighted_sentiment_zht = (-15, 15)
    picsize = (40, 15)
    alltime = time_29 + time_30_03
elif mode == 'all':
    file_path_en = basic_path + "/../preprocessing/en.jsonl"
    file_path_zh = basic_path + "/../preprocessing/zh.jsonl"
    file_result = basic_path + "/result"
    process_path(file_result)
    """ if mode == 'all': """
    file_result_all = file_result + "/all"
    os.mkdir(file_result_all)
    scale_number_en_all = (0, 10000)
    scale_number_zh_all = (0, 250)
    scale_number_zhs_all = (0, 250)
    scale_number_zht_all = (0, 140)
    scale_sentiment_en_all = (-4500, 1000)
    scale_sentiment_zh_all = (-150, 100)
    scale_sentiment_zhs_all = (-80, 80)
    scale_sentiment_zht_all = (-140, 80)
    scale_weighted_sentiment_en_all = (-20000000, 150000000)
    scale_weighted_sentiment_zh_all = (-1200000,700000)
    scale_weighted_sentiment_zhs_all = (-1000000,550000)
    scale_weighted_sentiment_zht_all = (-450000,900000)
    picsize_all = (70, 15)
    alltime_all = all_time
    """ elif mode == '29': """
    file_result_29 = file_result + "/29"
    os.mkdir(file_result_29)
    scale_number_en_29 = (0, 500)
    scale_number_zh_29 = (0, 100)
    scale_number_zhs_29 = (0, 30)
    scale_number_zht_29 = (0, 70)
    scale_sentiment_en_29 = (-50, 100)
    scale_sentiment_zh_29 = (-15, 90)
    scale_sentiment_zhs_29 = (-5, 20)
    scale_sentiment_zht_29 = (-10, 70)
    scale_weighted_sentiment_en_29 = (-150000000, 60000000)
    scale_weighted_sentiment_zh_29 = (-1000000,900000)
    scale_weighted_sentiment_zhs_29 = (-500000,500000)
    scale_weighted_sentiment_zht_29 = (-500000,400000)
    picsize_29 = (30, 15)
    alltime_29 = time_29
    """ elif mode == '30_03': """
    file_result_30_03 = file_result + "/30_03"
    os.mkdir(file_result_30_03)
    scale_number_en_30_03 = (0, 10000)
    scale_number_zh_30_03 = (0, 300)
    scale_number_zhs_30_03 = (0, 250)
    scale_number_zht_30_03 = (0, 25)
    scale_sentiment_en_30_03 = (-5000, 2000)
    scale_sentiment_zh_30_03 = (-50, 100)
    scale_sentiment_zhs_30_03 = (-40, 70)
    scale_sentiment_zht_30_03 = (-20, 30)
    scale_weighted_sentiment_en_30_03 = (-150000000, 60000000)
    scale_weighted_sentiment_zh_30_03 = (-1000000,900000)
    scale_weighted_sentiment_zhs_30_03 = (-500000,500000)
    scale_weighted_sentiment_zht_30_03 = (-500000,400000)
    picsize_30_03 = (40, 15)
    alltime_30_03 = time_30_03
    """ elif mode == '05_08': """
    file_result_05_08 = file_result + "/05_08"
    os.mkdir(file_result_05_08)
    scale_number_en_05_08 = (0, 500)
    scale_number_zh_05_08 = (0, 200)
    scale_number_zhs_05_08 = (0, 70)
    scale_number_zht_05_08 = (0, 130)
    scale_sentiment_en_05_08 = (-300, 200)
    scale_sentiment_zh_05_08 = (-200, 140)
    scale_sentiment_zhs_05_08 = (-70, 70)
    scale_sentiment_zht_05_08 = (-130, 70)
    scale_weighted_sentiment_en_05_08 = (-150000000, 60000000)
    scale_weighted_sentiment_zh_05_08 = (-1000000,900000)
    scale_weighted_sentiment_zhs_05_08 = (-500000,500000)
    scale_weighted_sentiment_zht_05_08 = (-500000,400000)
    picsize_05_08 = (40, 15)
    alltime_05_08 = time_05_08
    """ elif mode == '29_03': """
    file_result_29_03 = file_result + "/29_03"
    os.mkdir(file_result_29_03)
    scale_number_en_29_03 = (0, 10000)
    scale_number_zh_29_03 = (0, 400)
    scale_number_zhs_29_03 = (0, 250)
    scale_number_zht_29_03 = (0, 130)
    scale_sentiment_en_29_03 = (-5000, 2000)
    scale_sentiment_zh_29_03 = (-160, 140)
    scale_sentiment_zhs_29_03 = (-25, 70)
    scale_sentiment_zht_29_03 = (-130, 70)
    scale_weighted_sentiment_en_29_03 = (-150000000, 60000000)
    scale_weighted_sentiment_zh_29_03 = (-1000000,900000)
    scale_weighted_sentiment_zhs_29_03 = (-500000,500000)
    scale_weighted_sentiment_zht_29_03 = (-500000,400000)
    picsize_29_03 = (40, 15)
    alltime_29_03 = time_29 + time_30_03
    """ elif mode == '30_08': """
    file_result_30_08 = file_result + "/30_08"
    os.mkdir(file_result_30_08)
    scale_number_en_30_08 = (0, 10000)
    scale_number_zh_30_08 = (0, 400)
    scale_number_zhs_30_08 = (0, 250)
    scale_number_zht_30_08 = (0, 130)
    scale_sentiment_en_30_08 = (-5000, 2000)
    scale_sentiment_zh_30_08 = (-170, 140)
    scale_sentiment_zhs_30_08 = (-40, 70)
    scale_sentiment_zht_30_08 = (-130, 70)
    scale_weighted_sentiment_en_30_08 = (-20000000, 100000000)
    scale_weighted_sentiment_zh_30_08 = (-1100000,700000)
    scale_weighted_sentiment_zhs_30_08 = (-800000,550000)
    scale_weighted_sentiment_zht_30_08 = (-450000,600000)
    picsize_30_08 = (80, 15)
    alltime_30_08 = time_30_03 + time_05_08
else:
    raise ValueError('Wrong Mode')

scale_tripic = (-1.2, 1.2)
thuseg = thulac.thulac(seg_only=True, filt = False)

def gettime(text):
    # if text[4] == "S":
    #     t_month = "09"
    # elif text[4] == "O":
    #     t_month = "10"
    # else:
    #     raise ValueError("Month Error")
    t_month = text[4:7]
    t_day = text[8:10]
    if int(text[11:13]) + 8 <= 23:
        t_hour = str(int(text[11:13]) + 8)
    else:
        t_hour = str(int(text[11:13]) - 16)
        if t_day == '30':
            t_month = 'Oct'
            t_day = '01'
        else:
            t_day = '0' + str(int(t_day) + 1)
    t = t_month + '-' + t_day + ' ' + t_hour + 'h'
    # print ("time: ", t)
    return t

def getminute(text, t_minute_max, t_minute_min):
    t_minute = text[14:16]
    if int(t_minute) > int(t_minute_max):
        t_minute_max = str(t_minute)
    if int(t_minute) < int(t_minute_min):
        t_minute_min = str(t_minute)
    return t_minute_max, t_minute_min

def correctnumber(max_time_record, min_time_record, number_record, filename, lang, correct_number = False):
    return number_record

def delurl(text, url):
    for i in range (len(url)):
        text = text.replace(str(url[i]), '')
    return text

def dataprep(text, lang):
    url = re.findall(r'http[a-zA-Z0-9\.\?\/\&\=\:\^\%\$\#\!]*', text)
    text = delurl(text, url)
    if lang == 'zh':
        text = thuseg.cut(text, text=True)
    text = text.replace("\n", "\0")
    return text

def location(tweets, locat):
    modified = 0
    if tweets['user']['location'] != None:
        for items in locat:
            if str(items) == tweets['user']['location']:
                locat[str(items)] = locat[str(items)] + 1
                modified = 1
        if modified == 0:
            locat[tweets['user']['location']] = 1
    return locat

def normalized_data(number_record, sentiment_record_pos, sentiment_record_neg):
    for items in sentiment_record_pos:
        # print ("item: ", items)
        if number_record[items] != '0':
            sentiment_record_pos[items] = str(float(sentiment_record_pos[items]) / float(number_record[items]))
        elif sentiment_record_pos[items] != '0':
            raise ValueError("Sentiment Score Error")
    for items in sentiment_record_neg:
        # print ("item: ", items)
        if number_record[items] != '0':
            sentiment_record_neg[items] = str(float(sentiment_record_neg[items]) / float(number_record[items]))
        elif sentiment_record_neg[items] != '0':
            raise ValueError("Sentiment Score Error")
    sentiment_record_normal = {}
    for items in sentiment_record_pos:
        sentiment_record_normal[items] = str(float(sentiment_record_pos[items]) - float(sentiment_record_neg[items]))
    return sentiment_record_pos, sentiment_record_neg, sentiment_record_normal

def drawwordcloud(text, file_target):
    font = basic_path + '/simfang.ttf'
    wordcloud = WordCloud(background_color="white", font_path=font, collocations=False, width=1000, height=860, margin=2).generate(text)
    wordcloud.to_file(file_target)

def drawpic(h, record, picname, xname, yname, Ylim, picsize, file_target):
    y = []
    for t in h:
        y.append(float(record[t]))
    lenh = range(len(h))
    # print ('h = ', h)
    # print ('y = ', y)
    plt.figure(figsize = picsize)
    plt.plot(lenh, y, linewidth = 3, color = 'blue')
    plt.xticks(lenh, h, rotation = 45)
    plt.tick_params(axis='x', labelsize = 16)
    plt.tick_params(axis='y', labelsize = 25)
    plt.ylim(Ylim)
    font_x = {'family': 'Times New Roman', 'weight': 'normal', 'size'   : 28}
    font_y = {'family': 'Times New Roman', 'weight': 'normal', 'size'   : 28}
    font_title = {'family': 'Times New Roman', 'weight': 'normal', 'size'   : 40}
    plt.xlabel(xname, font_x)
    plt.ylabel(yname, font_y)
    plt.title(picname, font_title)
    # for a, b in zip(lenh, y):
    #     plt.text(a, b, b, ha='center', va='bottom', fontsize=20)
    plt.savefig(file_target + "/{}.jpg".format(picname))
    plt.clf()

def drawtripic(h, record1, record2, record3, picname, xname, yname, Ylim, picsize, file_target):
    y1 = []
    y2 = []
    y3 = []
    for t in h:
        y1.append(float(record1[t]))
        y2.append(float(record2[t]))
        y3.append(float(record3[t]))
    lenh = range(len(h))
    # print ('h = ', h)
    # print ('y = ', y)
    plt.figure(figsize = picsize)
    plt.plot(lenh, y1, linewidth = 3, color = 'blue', label='Positive Percentage')
    plt.plot(lenh, y2, linewidth = 3, color = 'green', label='Negative Percentage')
    plt.plot(lenh, y3, linewidth = 3, color = 'red', label='Overall Sentiment')
    plt.xticks(lenh, h, rotation = 45)
    plt.tick_params(axis='x', labelsize = 16)
    plt.tick_params(axis='y', labelsize = 25)
    plt.ylim(Ylim)
    font_x = {'family': 'Times New Roman', 'weight': 'normal', 'size'   : 28}
    font_y = {'family': 'Times New Roman', 'weight': 'normal', 'size'   : 28}
    font_title = {'family': 'Times New Roman', 'weight': 'normal', 'size'   : 40}
    plt.xlabel(xname, font_x)
    plt.ylabel(yname, font_y)
    plt.title(picname, font_title)
    plt.legend()
    plt.savefig(file_target + "/{}.jpg".format(picname))
    plt.clf()

def drawallpic(time_period, number_record_corrected_en, number_record_corrected_zh, number_record_corrected_zhs, number_record_corrected_zht, sentiment_record_corrected_en, 
    sentiment_record_corrected_zh, sentiment_record_corrected_zhs, sentiment_record_corrected_zht, sentiment_record_weight_corrected_en, sentiment_record_weight_corrected_zh, 
    sentiment_record_weight_corrected_zhs, sentiment_record_weight_corrected_zht, sentiment_record_pos_en, sentiment_record_neg_en, sentiment_record_normal_en,
    sentiment_record_pos_zh, sentiment_record_neg_zh, sentiment_record_normal_zh, sentiment_record_pos_zhs, sentiment_record_neg_zhs, sentiment_record_normal_zhs, 
    sentiment_record_pos_zht, sentiment_record_neg_zht, sentiment_record_normal_zht, sentiment_record_weight_pos_en, sentiment_record_weight_neg_en, sentiment_record_weight_normal_en, 
    sentiment_record_weight_pos_zh, sentiment_record_weight_neg_zh, sentiment_record_weight_normal_zh, sentiment_record_weight_pos_zhs, sentiment_record_weight_neg_zhs, 
    sentiment_record_weight_normal_zhs, sentiment_record_weight_pos_zht, sentiment_record_weight_neg_zht, sentiment_record_weight_normal_zht, scale_number_en, scale_number_zh, 
    scale_number_zhs, scale_number_zht, scale_sentiment_en, scale_sentiment_zh, scale_sentiment_zhs, scale_sentiment_zht, scale_weighted_sentiment_en, scale_weighted_sentiment_zh, 
    scale_weighted_sentiment_zhs, scale_weighted_sentiment_zht, scale_tripic, picsize, file_target):

    drawpic(time_period, number_record_corrected_en, "Number of Tweets by Time (English)", "Time", "Number", scale_number_en, picsize, file_target)
    drawpic(time_period, number_record_corrected_zh, "Number of Tweets by Time (Chinese)", "Time", "Number", scale_number_zh, picsize, file_target)
    drawpic(time_period, number_record_corrected_zhs, "Number of Tweets by Time (Simplified Chinese)", "Time", "Number", scale_number_zhs, picsize, file_target)
    drawpic(time_period, number_record_corrected_zht, "Number of Tweets by Time (Traditional Chinese)", "Time", "Number", scale_number_zht, picsize, file_target)

    drawpic(time_period, sentiment_record_corrected_en, "Sentiment of Tweets by Time (English)", "Time", "Sentiment", scale_sentiment_en, picsize, file_target)
    drawpic(time_period, sentiment_record_corrected_zh, "Sentiment of Tweets by Time (Chinese)", "Time", "Sentiment", scale_sentiment_zh, picsize, file_target)
    drawpic(time_period, sentiment_record_corrected_zhs, "Sentiment of Tweets by Time (Simplified Chinese)", "Time", "Sentiment", scale_sentiment_zhs, picsize, file_target)
    drawpic(time_period, sentiment_record_corrected_zht, "Sentiment of Tweets by Time (Traditional Chinese)", "Time", "Sentiment", scale_sentiment_zht, picsize, file_target)

    drawpic(time_period, sentiment_record_weight_corrected_en, "Weighted Sentiment of Tweets by Time (English)", "Time", "Sentiment", scale_weighted_sentiment_en, picsize, file_target)
    drawpic(time_period, sentiment_record_weight_corrected_zh, "Weighted Sentiment of Tweets by Time (Chinese)", "Time", "Sentiment", scale_weighted_sentiment_zh, picsize, file_target)
    drawpic(time_period, sentiment_record_weight_corrected_zhs, "Weighted Sentiment of Tweets by Time (Simplified Chinese)", "Time", "Sentiment", scale_weighted_sentiment_zhs, picsize, file_target)
    drawpic(time_period, sentiment_record_weight_corrected_zht, "Weighted Sentiment of Tweets by Time (Traditional Chinese)", "Time", "Sentiment", scale_weighted_sentiment_zht, picsize, file_target)

    drawtripic(time_period, sentiment_record_pos_en, sentiment_record_neg_en, sentiment_record_normal_en, "Normalized Sentiment of Tweets by Time (English)", "Time", "Sentiment", scale_tripic, picsize, file_target)
    drawtripic(time_period, sentiment_record_pos_zh, sentiment_record_neg_zh, sentiment_record_normal_zh, "Normalized Sentiment of Tweets by Time (Chinese)", "Time", "Sentiment", scale_tripic, picsize, file_target)
    drawtripic(time_period, sentiment_record_pos_zhs, sentiment_record_neg_zhs, sentiment_record_normal_zhs, "Normalized Sentiment of Tweets by Time (Simplified Chinese)", "Time", "Sentiment", scale_tripic, picsize, file_target)
    drawtripic(time_period, sentiment_record_pos_zht, sentiment_record_neg_zht, sentiment_record_normal_zht, "Normalized Sentiment of Tweets by Time (Traditional Chinese)", "Time", "Sentiment", scale_tripic, picsize, file_target)

    drawtripic(time_period, sentiment_record_weight_pos_en, sentiment_record_weight_neg_en, sentiment_record_weight_normal_en, "Normalized Weighted Sentiment of Tweets by Time (English)", "Time", "Sentiment", scale_tripic, picsize, file_target)
    drawtripic(time_period, sentiment_record_weight_pos_zh, sentiment_record_weight_neg_zh, sentiment_record_weight_normal_zh, "Normalized Weighted Sentiment of Tweets by Time (Chinese)", "Time", "Sentiment", scale_tripic, picsize, file_target)
    drawtripic(time_period, sentiment_record_weight_pos_zhs, sentiment_record_weight_neg_zhs, sentiment_record_weight_normal_zhs, "Normalized Weighted Sentiment of Tweets by Time (Simplified Chinese)", "Time", "Sentiment", scale_tripic, picsize, file_target)
    drawtripic(time_period, sentiment_record_weight_pos_zht, sentiment_record_weight_neg_zht, sentiment_record_weight_normal_zht, "Normalized Weighted Sentiment of Tweets by Time (Traditional Chinese)", "Time", "Sentiment", scale_tripic, picsize, file_target)

def words_frequency(inputfile, outputfile):
    print (outputfile)
    wordlist = inputfile.split()
    counted_words = []
    words_count = {}
    for i in range(len(wordlist)):
        if wordlist[i] not in counted_words:
            counted_words.append(wordlist[i])
            words_count[wordlist[i]] = 1
            for j in range(i+1, len(wordlist)):
                if wordlist[i] == wordlist[j]:
                    words_count[wordlist[i]] += 1
    words = []
    counts = []
    for items in words_count:
        words.append(items)
        counts.append(words_count[items])
    combined = list(zip(words, counts))
    for k in range(len(combined)-1):
        for i in range(len(combined)-1):
            if combined[i][1] < combined[i+1][1]:
                variable = combined[i]
                combined[i] = combined[i+1]
                combined[i+1] = variable
    with open (file_result + "/{}.txt".format(outputfile), "w") as file:
        file.write(str(combined))

count_en = 0
# alltime_en = alltime
max_time_record_en = {}
min_time_record_en = {}
number_record_en = {}
number_record_weight_en = {}
sentiment_record_en = {}
sentiment_record_pos_en = {}
sentiment_record_neg_en = {}
sentiment_record_weight_en = {}
sentiment_record_weight_pos_en = {}
sentiment_record_weight_neg_en = {}
tweets_pos_en = ''
tweets_neg_en = ''
pos_location_en = {}
neg_location_en = {}
for times in all_time:
    max_time_record_en[times] = '0'
    min_time_record_en[times] = '59'
    number_record_en[times] = '0'
    number_record_weight_en[times] = '0'
    sentiment_record_en[times] = '0'
    sentiment_record_pos_en[times] = '0'
    sentiment_record_neg_en[times] = '0'
    sentiment_record_weight_en[times] = '0'
    sentiment_record_weight_pos_en[times] = '0'
    sentiment_record_weight_neg_en[times] = '0'
with open (file_path_en, "r") as f:
    for tweets in jsonlines.Reader(f):
        text = dataprep(tweets['text'], 'en')
        if text[0:2] == 'RT':
            text_delRT = text[3:]
        else:
            text_delRT = text
        rele_en = Classify_rele_en.test_twitter_rele_en(text, basic_path + "/rele_en")
        # print ("rele_en = ", rele_en)
        if rele_en == 1:
            count_en += 1
            time = gettime(tweets['created_at'])
            max_time_record_en[time], min_time_record_en[time] = getminute(tweets['created_at'], max_time_record_en[time], min_time_record_en[time])
            weight = tweets['user']['followers_count']
            # if time not in alltime_en:
            #     alltime_en.append(time)
            #     number_record_en[time] = '0'
            #     sentiment_record_en[time] = '0'
            #     sentiment_record_pos_en[time] = '0'
            #     sentiment_record_neg_en[time] = '0'
            # print ("alltime_en: ", alltime_en)
            number_record_en[time] = str(int(number_record_en[time]) + 1)
            number_record_weight_en[time] = str(int(number_record_weight_en[time]) + weight)
            sentiment_en = Classify_sentiment_en.test_twitter_sentiment_en(text, basic_path + "/sentiment_en")
            # print ("sentiment_en = ", sentiment_en)
            if sentiment_en == 1:
                sentiment_posneg_en = Classify_sentiment_posneg_en.test_twitter_sentiment_posneg(text, basic_path + "/sentiment_posneg_en")
                if sentiment_posneg_en == 1:
                    sentiment_record_pos_en[time] = str(int(sentiment_record_pos_en[time]) + 1)
                    # print ("sentiment_record_pos_en[", time,  "] = ", sentiment_record_pos_en[time])
                    sentiment_record_en[time] = str(int(sentiment_record_en[time]) + 1)
                    sentiment_record_weight_pos_en[time] = str(int(sentiment_record_weight_pos_en[time]) + weight)
                    sentiment_record_weight_en[time] = str(int(sentiment_record_weight_en[time]) + weight)
                    tweets_pos_en = tweets_pos_en + ' ' + text_delRT
                    pos_location_en = location(tweets, pos_location_en)
                elif sentiment_posneg_en == 0:
                    sentiment_record_neg_en[time] = str(int(sentiment_record_neg_en[time]) + 1)
                    # print ("sentiment_record_neg_en[", time,  "] = ", sentiment_record_neg_en[time])
                    sentiment_record_en[time] = str(int(sentiment_record_en[time]) - 1)
                    sentiment_record_weight_neg_en[time] = str(int(sentiment_record_weight_neg_en[time]) + weight)
                    sentiment_record_weight_en[time] = str(int(sentiment_record_weight_en[time]) - weight)
                    tweets_neg_en = tweets_neg_en + ' ' + text_delRT
                    neg_location_en = location(tweets, neg_location_en)
                else:
                    raise ValueError("Sentiment PosNeg Error")

count_zhs = 0
count_zht = 0
# alltime_zhs = alltime
# alltime_zht = alltime
max_time_record_zh = {}
min_time_record_zh = {}
number_record_zh = {}
number_record_weight_zh = {}
sentiment_record_zh = {}
sentiment_record_pos_zh = {}
sentiment_record_neg_zh = {}
sentiment_record_weight_zh = {}
sentiment_record_weight_pos_zh = {}
sentiment_record_weight_neg_zh = {}
tweets_pos_zh = ''
tweets_neg_zh = ''
pos_location_zh = {}
neg_location_zh = {}
max_time_record_zhs = {}
min_time_record_zhs = {}
number_record_zhs = {}
number_record_weight_zhs = {}
sentiment_record_zhs = {}
sentiment_record_pos_zhs = {}
sentiment_record_neg_zhs = {}
sentiment_record_weight_zhs = {}
sentiment_record_weight_pos_zhs = {}
sentiment_record_weight_neg_zhs = {}
tweets_pos_zhs = ''
tweets_neg_zhs = ''
pos_location_zhs = {}
neg_location_zhs = {}
max_time_record_zht = {}
min_time_record_zht = {}
number_record_zht = {}
number_record_weight_zht = {}
sentiment_record_zht = {}
sentiment_record_pos_zht = {}
sentiment_record_neg_zht = {}
sentiment_record_weight_zht = {}
sentiment_record_weight_pos_zht = {}
sentiment_record_weight_neg_zht = {}
tweets_pos_zht = ''
tweets_neg_zht = ''
pos_location_zht = {}
neg_location_zht = {}
for times in all_time:
    max_time_record_zh[times] = '0'
    min_time_record_zh[times] = '59'
    number_record_zh[times] = '0'
    number_record_weight_zh[times] = '0'
    sentiment_record_zh[times] = '0'
    sentiment_record_pos_zh[times] = '0'
    sentiment_record_neg_zh[times] = '0'
    sentiment_record_weight_zh[times] = '0'
    sentiment_record_weight_pos_zh[times] = '0'
    sentiment_record_weight_neg_zh[times] = '0'
    max_time_record_zhs[times] = '0'
    min_time_record_zhs[times] = '59'
    number_record_zhs[times] = '0'
    number_record_weight_zhs[times] = '0'
    sentiment_record_zhs[times] = '0'
    sentiment_record_pos_zhs[times] = '0'
    sentiment_record_neg_zhs[times] = '0'
    sentiment_record_weight_zhs[times] = '0'
    sentiment_record_weight_pos_zhs[times] = '0'
    sentiment_record_weight_neg_zhs[times] = '0'
# for times in all_time:
    max_time_record_zht[times] = '0'
    min_time_record_zht[times] = '59'
    number_record_zht[times] = '0'
    number_record_weight_zht[times] = '0'
    sentiment_record_zht[times] = '0'
    sentiment_record_pos_zht[times] = '0'
    sentiment_record_neg_zht[times] = '0'
    sentiment_record_weight_zht[times] = '0'
    sentiment_record_weight_pos_zht[times] = '0'
    sentiment_record_weight_neg_zht[times] = '0'
with open (file_path_zh, "r") as f:
    for tweets in jsonlines.Reader(f):
        text = dataprep(tweets['text'], 'zh')
        if text[0:2] == 'RT':
            text_delRT = text[3:]
        else:
            text_delRT = text
        rele = Classify_rele.test_twitter_rele(text, basic_path + "/rele")
        # print ("rele = ", rele)
        if rele == 1:
            time = gettime(tweets['created_at'])
            ctype = Classify_type.test_twitter_type(text, basic_path + "/type")
            # print ("type = ", ctype)
            max_time_record_zh[time], min_time_record_zh[time] = getminute(tweets['created_at'], max_time_record_zh[time], min_time_record_zh[time])
            number_record_zh[time] = str(int(number_record_zh[time]) + 1)
            weight = tweets['user']['followers_count']
            number_record_weight_zh[time] = str(int(number_record_weight_zh[time]) + weight)
            if ctype == 1:
                count_zhs += 1
                # if time not in alltime_zhs:
                #     alltime_zhs.append(time)
                #     number_record_zhs[time] = '0'
                #     sentiment_record_zhs[time] = '0'
                #     sentiment_record_pos_zhs[time] = '0'
                #     sentiment_record_neg_zhs[time] = '0'
                # print ("alltime_zhs: ", alltime_zhs)
                max_time_record_zhs[time], min_time_record_zhs[time] = getminute(tweets['created_at'], max_time_record_zhs[time], min_time_record_zhs[time])
                number_record_zhs[time] = str(int(number_record_zhs[time]) + 1)
                number_record_weight_zhs[time] = str(int(number_record_weight_zhs[time]) + weight)
                sentiment = Classify_sentiment.test_twitter_sentiment(text, basic_path + "/sentiment")
                # print ("sentiment = ", sentiment)
                if sentiment == 1:
                    sentiment_posneg = Classify_sentiment_posneg.test_twitter_sentiment_posneg(text, basic_path + "/sentiment_posneg")
                    # print ("sentiment_posneg = ", sentiment_posneg)
                    if sentiment_posneg == 1:
                        sentiment_record_pos_zh[time] = str(int(sentiment_record_pos_zh[time]) + 1)
                        sentiment_record_pos_zhs[time] = str(int(sentiment_record_pos_zhs[time]) + 1)
                        sentiment_record_zh[time] = str(int(sentiment_record_zh[time]) + 1)
                        sentiment_record_zhs[time] = str(int(sentiment_record_zhs[time]) + 1)
                        sentiment_record_weight_pos_zh[time] = str(int(sentiment_record_weight_pos_zh[time]) + weight)
                        sentiment_record_weight_pos_zhs[time] = str(int(sentiment_record_weight_pos_zhs[time]) + weight)
                        sentiment_record_weight_zh[time] = str(int(sentiment_record_weight_zh[time]) + weight)
                        sentiment_record_weight_zhs[time] = str(int(sentiment_record_weight_zhs[time]) + weight)
                        tweets_pos_zh = tweets_pos_zh + ' ' + text_delRT
                        tweets_pos_zhs = tweets_pos_zhs + ' ' + text_delRT
                        pos_location_zh = location(tweets, pos_location_zh)
                        pos_location_zhs = location(tweets, pos_location_zhs)
                    elif sentiment_posneg == 0:
                        sentiment_record_neg_zh[time] = str(int(sentiment_record_neg_zh[time]) + 1)
                        sentiment_record_neg_zhs[time] = str(int(sentiment_record_neg_zhs[time]) + 1)
                        sentiment_record_zh[time] = str(int(sentiment_record_zh[time]) - 1)
                        sentiment_record_zhs[time] = str(int(sentiment_record_zhs[time]) - 1)
                        sentiment_record_weight_neg_zh[time] = str(int(sentiment_record_weight_neg_zh[time]) + weight)
                        sentiment_record_weight_neg_zhs[time] = str(int(sentiment_record_weight_neg_zhs[time]) + weight)
                        sentiment_record_weight_zh[time] = str(int(sentiment_record_weight_zh[time]) - weight)
                        sentiment_record_weight_zhs[time] = str(int(sentiment_record_weight_zhs[time]) - weight)
                        tweets_neg_zh = tweets_neg_zh + ' ' + text_delRT
                        tweets_neg_zhs = tweets_neg_zhs + ' ' + text_delRT
                        neg_location_zh = location(tweets, neg_location_zh)
                        neg_location_zhs = location(tweets, neg_location_zhs)
                    else:
                        raise ValueError("Sentiment PosNeg Error")
            elif ctype == 0:
                count_zht += 1
                # if time not in alltime_zht:
                #     alltime_zht.append(time)
                #     number_record_zht[time] = '0'
                #     sentiment_record_zht[time] = '0'
                #     sentiment_record_pos_zht[time] = '0'
                #     sentiment_record_neg_zht[time] = '0'
                # print ("alltime_zht: ", alltime_zht)
                max_time_record_zht[time], min_time_record_zht[time] = getminute(tweets['created_at'], max_time_record_zht[time], min_time_record_zht[time])
                number_record_zht[time] = str(int(number_record_zht[time]) + 1)
                number_record_weight_zht[time] = str(int(number_record_weight_zht[time]) + weight)
                sentiment = Classify_sentiment.test_twitter_sentiment(text, basic_path + "/sentiment")
                # print ("sentiment = ", sentiment)
                if sentiment == 1:
                    sentiment_posneg = Classify_sentiment_posneg.test_twitter_sentiment_posneg(text, basic_path + "/sentiment_posneg")
                    # print ("sentiment_posneg = ", sentiment_posneg)
                    if sentiment_posneg == 1:
                        sentiment_record_pos_zh[time] = str(int(sentiment_record_pos_zh[time]) + 1)
                        sentiment_record_pos_zht[time] = str(int(sentiment_record_pos_zht[time]) + 1)
                        sentiment_record_zh[time] = str(int(sentiment_record_zh[time]) + 1)
                        sentiment_record_zht[time] = str(int(sentiment_record_zht[time]) + 1)
                        sentiment_record_weight_pos_zh[time] = str(int(sentiment_record_weight_pos_zh[time]) + weight)
                        sentiment_record_weight_pos_zht[time] = str(int(sentiment_record_weight_pos_zht[time]) + weight)
                        sentiment_record_weight_zh[time] = str(int(sentiment_record_weight_zh[time]) + weight)
                        sentiment_record_weight_zht[time] = str(int(sentiment_record_weight_zht[time]) + weight)
                        tweets_pos_zh = tweets_pos_zh + ' ' + text_delRT
                        tweets_pos_zht = tweets_pos_zht + ' ' + text_delRT
                        pos_location_zh = location(tweets, pos_location_zh)
                        pos_location_zht = location(tweets, pos_location_zht)
                    elif sentiment_posneg == 0:
                        sentiment_record_neg_zh[time] = str(int(sentiment_record_neg_zh[time]) + 1)
                        sentiment_record_neg_zht[time] = str(int(sentiment_record_neg_zht[time]) + 1)
                        sentiment_record_zh[time] = str(int(sentiment_record_zh[time]) - 1)
                        sentiment_record_zht[time] = str(int(sentiment_record_zht[time]) - 1)
                        sentiment_record_weight_neg_zh[time] = str(int(sentiment_record_weight_neg_zh[time]) + weight)
                        sentiment_record_weight_neg_zht[time] = str(int(sentiment_record_weight_neg_zht[time]) + weight)
                        sentiment_record_weight_zh[time] = str(int(sentiment_record_weight_zh[time]) - weight)
                        sentiment_record_weight_zht[time] = str(int(sentiment_record_weight_zht[time]) - weight)
                        tweets_neg_zh = tweets_neg_zh + ' ' + text_delRT
                        tweets_neg_zht = tweets_neg_zht + ' ' + text_delRT
                        neg_location_zh = location(tweets, neg_location_zh)
                        neg_location_zht = location(tweets, neg_location_zht)
                    else:
                        raise ValueError("Sentiment PosNeg Error")
            else:
                raise ValueError("Character Type Error")

number_record_corrected_en = correctnumber(max_time_record_en, min_time_record_en, number_record_en, 'number_en', 'en', True)
number_record_corrected_zh = correctnumber(max_time_record_zh, min_time_record_zh, number_record_zh, 'number_zh', 'zh')
number_record_corrected_zhs = correctnumber(max_time_record_zhs, min_time_record_zhs, number_record_zhs, 'number_zhs', 'zhs')
number_record_corrected_zht = correctnumber(max_time_record_zht, min_time_record_zht, number_record_zht, 'number_zht', 'zht')

sentiment_record_corrected_en = correctnumber(max_time_record_en, min_time_record_en, sentiment_record_en, 'sentiment_en', 'en', True)
sentiment_record_corrected_zh = correctnumber(max_time_record_zh, min_time_record_zh, sentiment_record_zh, 'sentiment_zh', 'zh')
sentiment_record_corrected_zhs = correctnumber(max_time_record_zhs, min_time_record_zhs, sentiment_record_zhs, 'sentiment_zhs', 'zhs')
sentiment_record_corrected_zht = correctnumber(max_time_record_zht, min_time_record_zht, sentiment_record_zht, 'sentiment_zht', 'zht')

sentiment_record_weight_corrected_en = correctnumber(max_time_record_en, min_time_record_en, sentiment_record_weight_en, 'weighted_sentiment_en', 'en', True)
sentiment_record_weight_corrected_zh = correctnumber(max_time_record_zh, min_time_record_zh, sentiment_record_weight_zh, 'weighted_sentiment_zh', 'zh')
sentiment_record_weight_corrected_zhs = correctnumber(max_time_record_zhs, min_time_record_zhs, sentiment_record_weight_zhs, 'weighted_sentiment_zhs', 'zhs')
sentiment_record_weight_corrected_zht = correctnumber(max_time_record_zht, min_time_record_zht, sentiment_record_weight_zht, 'weighted_sentiment_zht', 'zht')

# with open (file_result + '/number_record_corrected_en.jsonl', 'w') as f:
#     f.write(json.dumps(number_record_corrected_en))
# with open (file_result + '/number_record_corrected_zhs.jsonl', 'w') as f:
#     f.write(json.dumps(number_record_corrected_zhs))
# with open (file_result + '/number_record_corrected_zht.jsonl', 'w') as f:
#     f.write(json.dumps(number_record_corrected_zht))

sentiment_record_pos_en, sentiment_record_neg_en, sentiment_record_normal_en = normalized_data(number_record_en, sentiment_record_pos_en, sentiment_record_neg_en)
sentiment_record_pos_zh, sentiment_record_neg_zh, sentiment_record_normal_zh = normalized_data(number_record_zh, sentiment_record_pos_zh, sentiment_record_neg_zh)
sentiment_record_pos_zhs, sentiment_record_neg_zhs, sentiment_record_normal_zhs = normalized_data(number_record_zhs, sentiment_record_pos_zhs, sentiment_record_neg_zhs)
sentiment_record_pos_zht, sentiment_record_neg_zht, sentiment_record_normal_zht = normalized_data(number_record_zht, sentiment_record_pos_zht, sentiment_record_neg_zht)

sentiment_record_weight_pos_en, sentiment_record_weight_neg_en, sentiment_record_weight_normal_en = normalized_data(number_record_weight_en, sentiment_record_weight_pos_en, sentiment_record_weight_neg_en)
sentiment_record_weight_pos_zh, sentiment_record_weight_neg_zh, sentiment_record_weight_normal_zh = normalized_data(number_record_weight_zh, sentiment_record_weight_pos_zh, sentiment_record_weight_neg_zh)
sentiment_record_weight_pos_zhs, sentiment_record_weight_neg_zhs, sentiment_record_weight_normal_zhs = normalized_data(number_record_weight_zhs, sentiment_record_weight_pos_zhs, sentiment_record_weight_neg_zhs)
sentiment_record_weight_pos_zht, sentiment_record_weight_neg_zht, sentiment_record_weight_normal_zht = normalized_data(number_record_weight_zht, sentiment_record_weight_pos_zht, sentiment_record_weight_neg_zht)

if mode == 'test_on_2000':
    drawallpic(alltime, number_record_corrected_en, number_record_corrected_zh, number_record_corrected_zhs, number_record_corrected_zht, sentiment_record_corrected_en, 
    sentiment_record_corrected_zh, sentiment_record_corrected_zhs, sentiment_record_corrected_zht, sentiment_record_weight_corrected_en, sentiment_record_weight_corrected_zh, 
    sentiment_record_weight_corrected_zhs, sentiment_record_weight_corrected_zht, sentiment_record_pos_en, sentiment_record_neg_en, sentiment_record_normal_en,
    sentiment_record_pos_zh, sentiment_record_neg_zh, sentiment_record_normal_zh, sentiment_record_pos_zhs, sentiment_record_neg_zhs, sentiment_record_normal_zhs, 
    sentiment_record_pos_zht, sentiment_record_neg_zht, sentiment_record_normal_zht, sentiment_record_weight_pos_en, sentiment_record_weight_neg_en, sentiment_record_weight_normal_en, 
    sentiment_record_weight_pos_zh, sentiment_record_weight_neg_zh, sentiment_record_weight_normal_zh, sentiment_record_weight_pos_zhs, sentiment_record_weight_neg_zhs, 
    sentiment_record_weight_normal_zhs, sentiment_record_weight_pos_zht, sentiment_record_weight_neg_zht, sentiment_record_weight_normal_zht, scale_number_en, scale_number_zh, 
    scale_number_zhs, scale_number_zht, scale_sentiment_en, scale_sentiment_zh, scale_sentiment_zhs, scale_sentiment_zht, scale_weighted_sentiment_en, scale_weighted_sentiment_zh, 
    scale_weighted_sentiment_zhs, scale_weighted_sentiment_zht, scale_tripic, picsize, file_result)
elif mode == 'all':
    """ if mode == 'all': """
    drawallpic(alltime_all, number_record_corrected_en, number_record_corrected_zh, number_record_corrected_zhs, number_record_corrected_zht, sentiment_record_corrected_en, 
    sentiment_record_corrected_zh, sentiment_record_corrected_zhs, sentiment_record_corrected_zht, sentiment_record_weight_corrected_en, sentiment_record_weight_corrected_zh, 
    sentiment_record_weight_corrected_zhs, sentiment_record_weight_corrected_zht, sentiment_record_pos_en, sentiment_record_neg_en, sentiment_record_normal_en,
    sentiment_record_pos_zh, sentiment_record_neg_zh, sentiment_record_normal_zh, sentiment_record_pos_zhs, sentiment_record_neg_zhs, sentiment_record_normal_zhs, 
    sentiment_record_pos_zht, sentiment_record_neg_zht, sentiment_record_normal_zht, sentiment_record_weight_pos_en, sentiment_record_weight_neg_en, sentiment_record_weight_normal_en, 
    sentiment_record_weight_pos_zh, sentiment_record_weight_neg_zh, sentiment_record_weight_normal_zh, sentiment_record_weight_pos_zhs, sentiment_record_weight_neg_zhs, 
    sentiment_record_weight_normal_zhs, sentiment_record_weight_pos_zht, sentiment_record_weight_neg_zht, sentiment_record_weight_normal_zht, scale_number_en_all, scale_number_zh_all, 
    scale_number_zhs_all, scale_number_zht_all, scale_sentiment_en_all, scale_sentiment_zh_all, scale_sentiment_zhs_all, scale_sentiment_zht_all, scale_weighted_sentiment_en_all, 
    scale_weighted_sentiment_zh_all, scale_weighted_sentiment_zhs_all, scale_weighted_sentiment_zht_all, scale_tripic, picsize_all, file_result_all)
    """ elif mode == '29': """
    drawallpic(alltime_29, number_record_corrected_en, number_record_corrected_zh, number_record_corrected_zhs, number_record_corrected_zht, sentiment_record_corrected_en, 
    sentiment_record_corrected_zh, sentiment_record_corrected_zhs, sentiment_record_corrected_zht, sentiment_record_weight_corrected_en, sentiment_record_weight_corrected_zh, 
    sentiment_record_weight_corrected_zhs, sentiment_record_weight_corrected_zht, sentiment_record_pos_en, sentiment_record_neg_en, sentiment_record_normal_en,
    sentiment_record_pos_zh, sentiment_record_neg_zh, sentiment_record_normal_zh, sentiment_record_pos_zhs, sentiment_record_neg_zhs, sentiment_record_normal_zhs, 
    sentiment_record_pos_zht, sentiment_record_neg_zht, sentiment_record_normal_zht, sentiment_record_weight_pos_en, sentiment_record_weight_neg_en, sentiment_record_weight_normal_en, 
    sentiment_record_weight_pos_zh, sentiment_record_weight_neg_zh, sentiment_record_weight_normal_zh, sentiment_record_weight_pos_zhs, sentiment_record_weight_neg_zhs, 
    sentiment_record_weight_normal_zhs, sentiment_record_weight_pos_zht, sentiment_record_weight_neg_zht, sentiment_record_weight_normal_zht, scale_number_en_29, scale_number_zh_29, 
    scale_number_zhs_29, scale_number_zht_29, scale_sentiment_en_29, scale_sentiment_zh_29, scale_sentiment_zhs_29, scale_sentiment_zht_29, scale_weighted_sentiment_en_29, 
    scale_weighted_sentiment_zh_29, scale_weighted_sentiment_zhs_29, scale_weighted_sentiment_zht_29, scale_tripic, picsize_29, file_result_29)
    """ elif mode == '30_03': """
    drawallpic(alltime_30_03, number_record_corrected_en, number_record_corrected_zh, number_record_corrected_zhs, number_record_corrected_zht, sentiment_record_corrected_en, 
    sentiment_record_corrected_zh, sentiment_record_corrected_zhs, sentiment_record_corrected_zht, sentiment_record_weight_corrected_en, sentiment_record_weight_corrected_zh, 
    sentiment_record_weight_corrected_zhs, sentiment_record_weight_corrected_zht, sentiment_record_pos_en, sentiment_record_neg_en, sentiment_record_normal_en,
    sentiment_record_pos_zh, sentiment_record_neg_zh, sentiment_record_normal_zh, sentiment_record_pos_zhs, sentiment_record_neg_zhs, sentiment_record_normal_zhs, 
    sentiment_record_pos_zht, sentiment_record_neg_zht, sentiment_record_normal_zht, sentiment_record_weight_pos_en, sentiment_record_weight_neg_en, sentiment_record_weight_normal_en, 
    sentiment_record_weight_pos_zh, sentiment_record_weight_neg_zh, sentiment_record_weight_normal_zh, sentiment_record_weight_pos_zhs, sentiment_record_weight_neg_zhs, 
    sentiment_record_weight_normal_zhs, sentiment_record_weight_pos_zht, sentiment_record_weight_neg_zht, sentiment_record_weight_normal_zht, scale_number_en_30_03, scale_number_zh_30_03, 
    scale_number_zhs_30_03, scale_number_zht_30_03, scale_sentiment_en_30_03, scale_sentiment_zh_30_03, scale_sentiment_zhs_30_03, scale_sentiment_zht_30_03, scale_weighted_sentiment_en_30_03, 
    scale_weighted_sentiment_zh_30_03, scale_weighted_sentiment_zhs_30_03, scale_weighted_sentiment_zht_30_03, scale_tripic, picsize_30_03, file_result_30_03)
    """ elif mode == '05_08': """
    drawallpic(alltime_05_08, number_record_corrected_en, number_record_corrected_zh, number_record_corrected_zhs, number_record_corrected_zht, sentiment_record_corrected_en, 
    sentiment_record_corrected_zh, sentiment_record_corrected_zhs, sentiment_record_corrected_zht, sentiment_record_weight_corrected_en, sentiment_record_weight_corrected_zh, 
    sentiment_record_weight_corrected_zhs, sentiment_record_weight_corrected_zht, sentiment_record_pos_en, sentiment_record_neg_en, sentiment_record_normal_en,
    sentiment_record_pos_zh, sentiment_record_neg_zh, sentiment_record_normal_zh, sentiment_record_pos_zhs, sentiment_record_neg_zhs, sentiment_record_normal_zhs, 
    sentiment_record_pos_zht, sentiment_record_neg_zht, sentiment_record_normal_zht, sentiment_record_weight_pos_en, sentiment_record_weight_neg_en, sentiment_record_weight_normal_en, 
    sentiment_record_weight_pos_zh, sentiment_record_weight_neg_zh, sentiment_record_weight_normal_zh, sentiment_record_weight_pos_zhs, sentiment_record_weight_neg_zhs, 
    sentiment_record_weight_normal_zhs, sentiment_record_weight_pos_zht, sentiment_record_weight_neg_zht, sentiment_record_weight_normal_zht, scale_number_en_05_08, scale_number_zh_05_08, 
    scale_number_zhs_05_08, scale_number_zht_05_08, scale_sentiment_en_05_08, scale_sentiment_zh_05_08, scale_sentiment_zhs_05_08, scale_sentiment_zht_05_08, scale_weighted_sentiment_en_05_08, 
    scale_weighted_sentiment_zh_05_08, scale_weighted_sentiment_zhs_05_08, scale_weighted_sentiment_zht_05_08, scale_tripic, picsize_05_08, file_result_05_08)
    """ elif mode == '29_03': """
    drawallpic(alltime_29_03, number_record_corrected_en, number_record_corrected_zh, number_record_corrected_zhs, number_record_corrected_zht, sentiment_record_corrected_en, 
    sentiment_record_corrected_zh, sentiment_record_corrected_zhs, sentiment_record_corrected_zht, sentiment_record_weight_corrected_en, sentiment_record_weight_corrected_zh, 
    sentiment_record_weight_corrected_zhs, sentiment_record_weight_corrected_zht, sentiment_record_pos_en, sentiment_record_neg_en, sentiment_record_normal_en,
    sentiment_record_pos_zh, sentiment_record_neg_zh, sentiment_record_normal_zh, sentiment_record_pos_zhs, sentiment_record_neg_zhs, sentiment_record_normal_zhs, 
    sentiment_record_pos_zht, sentiment_record_neg_zht, sentiment_record_normal_zht, sentiment_record_weight_pos_en, sentiment_record_weight_neg_en, sentiment_record_weight_normal_en, 
    sentiment_record_weight_pos_zh, sentiment_record_weight_neg_zh, sentiment_record_weight_normal_zh, sentiment_record_weight_pos_zhs, sentiment_record_weight_neg_zhs, 
    sentiment_record_weight_normal_zhs, sentiment_record_weight_pos_zht, sentiment_record_weight_neg_zht, sentiment_record_weight_normal_zht, scale_number_en_29_03, scale_number_zh_29_03, 
    scale_number_zhs_29_03, scale_number_zht_29_03, scale_sentiment_en_29_03, scale_sentiment_zh_29_03, scale_sentiment_zhs_29_03, scale_sentiment_zht_29_03, scale_weighted_sentiment_en_29_03, 
    scale_weighted_sentiment_zh_29_03, scale_weighted_sentiment_zhs_29_03, scale_weighted_sentiment_zht_29_03, scale_tripic, picsize_29_03, file_result_29_03)
    """ elif mode == '30_08': """
    drawallpic(alltime_30_08, number_record_corrected_en, number_record_corrected_zh, number_record_corrected_zhs, number_record_corrected_zht, sentiment_record_corrected_en, 
    sentiment_record_corrected_zh, sentiment_record_corrected_zhs, sentiment_record_corrected_zht, sentiment_record_weight_corrected_en, sentiment_record_weight_corrected_zh, 
    sentiment_record_weight_corrected_zhs, sentiment_record_weight_corrected_zht, sentiment_record_pos_en, sentiment_record_neg_en, sentiment_record_normal_en,
    sentiment_record_pos_zh, sentiment_record_neg_zh, sentiment_record_normal_zh, sentiment_record_pos_zhs, sentiment_record_neg_zhs, sentiment_record_normal_zhs, 
    sentiment_record_pos_zht, sentiment_record_neg_zht, sentiment_record_normal_zht, sentiment_record_weight_pos_en, sentiment_record_weight_neg_en, sentiment_record_weight_normal_en, 
    sentiment_record_weight_pos_zh, sentiment_record_weight_neg_zh, sentiment_record_weight_normal_zh, sentiment_record_weight_pos_zhs, sentiment_record_weight_neg_zhs, 
    sentiment_record_weight_normal_zhs, sentiment_record_weight_pos_zht, sentiment_record_weight_neg_zht, sentiment_record_weight_normal_zht, scale_number_en_30_08, scale_number_zh_30_08, 
    scale_number_zhs_30_08, scale_number_zht_30_08, scale_sentiment_en_30_08, scale_sentiment_zh_30_08, scale_sentiment_zhs_30_08, scale_sentiment_zht_30_08, scale_weighted_sentiment_en_30_08, 
    scale_weighted_sentiment_zh_30_08, scale_weighted_sentiment_zhs_30_08, scale_weighted_sentiment_zht_30_08, scale_tripic, picsize_30_08, file_result_30_08)
else:
    raise ValueError('Wrong Mode')

print ("count_en = ", count_en, "count_zhs = ", count_zhs, "count_zht = ", count_zht)

with open (file_result + "/number_record.jsonl", "w") as file:
    file.write(json.dumps(number_record_en) + '\n')
    file.write(json.dumps(number_record_zhs) + '\n')
    file.write(json.dumps(number_record_zht))

with open (file_result + "/sentiment_record.jsonl", "w") as file:
    file.write(json.dumps(sentiment_record_en) + '\n')
    file.write(json.dumps(sentiment_record_zhs) + '\n')
    file.write(json.dumps(sentiment_record_zht))

with open (file_result + "/pos_location_en.jsonl", "w") as file:
    file.write(json.dumps(pos_location_en))

with open (file_result + "/neg_location_en.jsonl", "w") as file:
    file.write(json.dumps(neg_location_en))

with open (file_result + "/pos_location_zh.jsonl", "w") as file:
    file.write(json.dumps(pos_location_zh))

with open (file_result + "/neg_location_zh.jsonl", "w") as file:
    file.write(json.dumps(neg_location_zh))

with open (file_result + "/pos_location_zhs.jsonl", "w") as file:
    file.write(json.dumps(pos_location_zhs))

with open (file_result + "/neg_location_zhs.jsonl", "w") as file:
    file.write(json.dumps(neg_location_zhs))

with open (file_result + "/pos_location_zht.jsonl", "w") as file:
    file.write(json.dumps(pos_location_zht))

with open (file_result + "/neg_location_zht.jsonl", "w") as file:
    file.write(json.dumps(neg_location_zht))

drawwordcloud(tweets_pos_en, file_result + "/tweets_pos_en.png")
drawwordcloud(tweets_neg_en, file_result + "/tweets_neg_en.png")
drawwordcloud(tweets_pos_zh, file_result + "/tweets_pos_zh.png")
drawwordcloud(tweets_neg_zh, file_result + "/tweets_neg_zh.png")
drawwordcloud(tweets_pos_zhs, file_result + "/tweets_pos_zhs.png")
drawwordcloud(tweets_neg_zhs, file_result + "/tweets_neg_zhs.png")
drawwordcloud(tweets_pos_zht, file_result + "/tweets_pos_zht.png")
drawwordcloud(tweets_neg_zht, file_result + "/tweets_neg_zht.png")

common_words_en = ['China', 'National', 'Day', 'day', '70th', 'People', '70year']
common_words_zh = ['中国', '国庆', '香港']
common_words_zhs = ['中国', '国庆']
common_words_zht = ['香港']

drawwordcloud(delurl(tweets_pos_en, common_words_en), file_result + "/tweets_pos_delcom_en.png")
drawwordcloud(delurl(tweets_neg_en, common_words_en), file_result + "/tweets_neg_delcom_en.png")
drawwordcloud(delurl(tweets_pos_zh, common_words_zh), file_result + "/tweets_pos_delcom_zh.png")
drawwordcloud(delurl(tweets_neg_zh, common_words_zh), file_result + "/tweets_neg_delcom_zh.png")
drawwordcloud(delurl(tweets_pos_zhs, common_words_zhs), file_result + "/tweets_pos_delcom_zhs.png")
drawwordcloud(delurl(tweets_neg_zhs, common_words_zhs), file_result + "/tweets_neg_delcom_zhs.png")
drawwordcloud(delurl(tweets_pos_zht, common_words_zht), file_result + "/tweets_pos_delcom_zht.png")
drawwordcloud(delurl(tweets_neg_zht, common_words_zht), file_result + "/tweets_neg_delcom_zht.png")

words_frequency(tweets_pos_en, 'counted_words_pos_en')
words_frequency(tweets_neg_en, 'counted_words_neg_en')
words_frequency(tweets_pos_zh, 'counted_words_pos_zh')
words_frequency(tweets_neg_zh, 'counted_words_neg_zh')
words_frequency(tweets_pos_zhs, 'counted_words_pos_zhs')
words_frequency(tweets_neg_zhs, 'counted_words_neg_zhs')
words_frequency(tweets_pos_zht, 'counted_words_pos_zht')
words_frequency(tweets_neg_zht, 'counted_words_neg_zht')