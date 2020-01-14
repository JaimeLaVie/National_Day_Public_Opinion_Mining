import os
import jsonlines
import json
import re

# 只收录带对勾的官方账号

knownmedia_china = {"PDChinese":{"screen_name":"PDChinese","name":"人民日報  People's Daily"}, "PDChina":{"screen_name":"PDChina","name":"People's Daily, China"},
            "globaltimesnews":{"screen_name":"globaltimesnews","name":"Global Times"}, "ChinaDaily":{"screen_name":"ChinaDaily","name":"China Daily"},
            "ChinaDailyAsia":{"screen_name":"ChinaDailyAsia","name":"China Daily Asia"}, "ChinaDaily":{"screen_name":"ChinaDaily","name":"China Daily"},
            "ChinaDaily":{"screen_name":"ChinaDaily","name":"China Daily"}, "XHNews":{"screen_name":"XHNews","name":"China Xinhua News"},
            "Echinanews":{"screen_name":"Echinanews","name":"China News 中国新闻网"}, "CCTV":{"screen_name":"CCTV","name":"CCTV"},
            "CGTNOfficial":{"screen_name":"CGTNOfficial","name":"CGTN"}, "ChinaPlusNews":{"screen_name":"ChinaPlusNews","name":"China Plus News"},
            "PhoenixTVHK":{"screen_name":"PhoenixTVHK","name":"PhoenixTV 鳳凰衛視"}}

knownmedia_china_hk = {"PhoenixTVHK":{"screen_name":"PhoenixTVHK","name":"PhoenixTV 鳳凰衛視"}}

knownmedia_usa = {"FoxNews":{"screen_name":"FoxNews","name":"Fox News"}, "CNN":{"screen_name":"CNN","name":"CNN"},
            "nytimes":{"screen_name":"nytimes","name":"The New York Times"},"cnnbrk":{"screen_name":"cnnbrk","name":"CNN Breaking News"},
            "nytchinese":{"screen_name":"nytchinese","name":"纽约时报中文网"}, "RFA_Chinese":{"screen_name":"RFA_Chinese","name":"自由亚洲电台"}, 
            "RfaCantonese":{"screen_name":"RfaCantonese","name":"RFA 自由亞洲粵語"}, "nypost":{"screen_name":"nypost","name":"New York Post"},
            "VOANews":{"screen_name":"VOANews","name":"The Voice of America"}, "voachina":{"screen_name":"voachina","name":"美国之音争鸣论坛"},
            "VOAChinese":{"screen_name":"VOAChinese","name":"美国之音中文网"}, "ChineseWSJ":{"screen_name":"ChineseWSJ","name":"华尔街日报中文网"},
            "WSJ":{"screen_name":"WSJ","name":"The Wall Street Journal"}, "washingtonpost":{"screen_name":"washingtonpost","name":"The Washington Post"},
            "USATODAY":{"screen_name":"USATODAY","name":"USA TODAY"}, "usatodayopinion":{"screen_name":"usatodayopinion","name":"USA TODAY Opinion"},
            "latimes":{"screen_name":"latimes","name":"Los Angeles Times"}, "latimesopinion":{"screen_name":"latimesopinion","name":"L.A. Times Opinion"},
            "EpochTimes":{"screen_name":"EpochTimes","name":"The Epoch Times"}, "EpochTimesChina":{"screen_name":"EpochTimesChina","name":"The Epoch Times - China Insider"}}

knownmedia_uk = {"BBC":{"screen_name":"BBC","name":"BBC"}, "BBCWorld":{"screen_name":"BBCWorld","name":"BBC News (World)"},
            "BBCNews":{"screen_name":"BBCNews","name":"BBC News (UK)"}, "bbcchinese":{"screen_name":"bbcchinese","name":"BBC News 中文"},
            "TheSun":{"screen_name":"TheSun","name":"The Sun"}, "TheEconomist":{"screen_name":"TheEconomist","name":"The Economist"},
            "thesundaytimes":{"screen_name":"thesundaytimes","name":"The Sunday Times"}, "DailyMirror":{"screen_name":"DailyMirror","name":"Daily Mirror"},
            "thetimes":{"screen_name":"thetimes","name":"The Times"}, "TheSundayMirror":{"screen_name":"TheSundayMirror","name":"Sunday Mirror"},
            "Telegraph":{"screen_name":"Telegraph","name":"The Telegraph"}, "thedailystar":{"screen_name":"thedailystar","name":"The Daily Star"},
            "dailystarnews":{"screen_name":"dailystarnews","name":"The Daily Star"}, "DailyStarSunday":{"screen_name":"DailyStarSunday","name":"Daily Star Sunday"}, 
            "dailystaruk":{"screen_name":"dailystaruk","name":"Daily Star UK"}, "guardian":{"screen_name":"guardian","name":"The Guardian"},
            "MailOnline":{"screen_name":"MailOnline","name":"Daily Mail Online"}, "DailyMailUK":{"screen_name":"DailyMailUK","name":"Daily Mail U.K."}}

basic_path = os.getcwd()
file_path_en = basic_path + "/preprocessing/en.jsonl"
file_path_zh = basic_path + "/preprocessing/zh.jsonl"
file_target = basic_path + "/preprocessing_media/"

def JudgeMedia(user):
    found = 0
    result = 'NotKnownMedia'
    for items in knownmedia_china:
        if knownmedia_china[items]['screen_name'] == user:
            result = 'China'
            found += 1
    for items in knownmedia_usa:
        if knownmedia_usa[items]['screen_name'] == user:
            result = 'USA'
            found += 1
    for items in knownmedia_uk:
        if knownmedia_uk[items]['screen_name'] == user:
            result = 'UK'
            found += 1
    assert (found == 0 and result == 'NotKnownMedia') or found == 1
    return result

def JudgeisRetweetMedia(text):
    # for i in range(len(text)):
    #     if text[i] == ':':
    #         mark = i
    #         break
    # try:
    #     return JudgeMedia(text[:mark])
    # except:
    #     print (text)
    #     return 'NotKnownMedia'
    found = 0
    result = 'NotKnownMedia'
    for items in knownmedia_china:
        if re.findall('RT @' + items + ':', text) != []:
            result = 'China'
            found += 1
    for items in knownmedia_usa:
        if re.findall('RT @' + items + ':', text) != []:
            result = 'USA'
            found += 1
    for items in knownmedia_uk:
        if re.findall('RT @' + items + ':', text) != []:
            result = 'UK'
            found += 1
    assert (found == 0 and result == 'NotKnownMedia') or found == 1
    return result

with open (file_path_en, "r") as f:
    print (file_path_en)
    for tweets in jsonlines.Reader(f):
        user = tweets['user']['screen_name']
        text = tweets['text']
        isMedia = JudgeMedia(user)
        with open (file_target + '{}_en.jsonl'.format(isMedia), "a") as file:
            file.write(json.dumps(tweets)+'\n')
        isKeyword = re.findall('RT @', text)
        # if text[0:2] == 'RT':
        if isKeyword != []:
            # isRetweetMedia = JudgeisRetweetMedia(text[4:])
            isRetweetMedia = JudgeisRetweetMedia(text)
            with open (file_target + '{}_en_retweet_media.jsonl'.format(isRetweetMedia), "a") as fr:
                fr.write(json.dumps(tweets)+'\n')

with open (file_path_zh, "r") as f:
    print (file_path_zh)
    for tweets in jsonlines.Reader(f):
        user = tweets['user']['screen_name']
        text = tweets['text']
        isMedia = JudgeMedia(user)
        with open (file_target + '{}_zh.jsonl'.format(isMedia), "a") as file:
            file.write(json.dumps(tweets)+'\n')
        isKeyword = re.findall('RT @', text)
        # if text[0:2] == 'RT':
        if isKeyword != []:
            # isRetweetMedia = JudgeisRetweetMedia(text[4:])
            isRetweetMedia = JudgeisRetweetMedia(text)
            with open (file_target + '{}_zh_retweet_media.jsonl'.format(isRetweetMedia), "a") as fr:
                fr.write(json.dumps(tweets)+'\n')