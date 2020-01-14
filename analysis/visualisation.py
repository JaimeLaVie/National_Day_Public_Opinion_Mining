import os
import jsonlines
from pyecharts import Map 
from pyecharts import Geo

# locations = {'China': {'Mainland': 0, 'Hong Kong': 0, 'Macau': 0, "Taiwan": 0}, 'United States': 0, "Russia": 0, "United Kingdom": 0, "France": 0, "Germany": 0, 
#             "Japan": 0, "Korea": 0, "Italy": 0, "Canada": 0, "Australia": 0, "New Zealand": 0, "Brazil": 0, "Vietnam": 0, "Malasia": 0, "Thailand": 0}

# locations = {'China': 0, 'United States': 0, "Russia": 0, "United Kingdom": 0, "France": 0, "Germany": 0, "Japan": 0, "Korea": 0, "Italy": 0, "Canada": 0, 
#             "Australia": 0, "New Zealand": 0, "Brazil": 0, "Vietnam": 0, "Malasia": 0, "Thailand": 0}

basic_path = os.getcwd()
file_path_pos_en = basic_path + "/locations/pos_location_en.jsonl"
file_path_neg_en = basic_path + "/locations/neg_location_en.jsonl"
file_path_pos_zh = basic_path + "/locations/pos_location_zh.jsonl"
file_path_neg_zh = basic_path + "/locations/neg_location_zh.jsonl"
file_path_pos_zhs = basic_path + "/locations/pos_location_zhs.jsonl"
file_path_neg_zhs = basic_path + "/locations/neg_location_zhs.jsonl"
file_path_pos_zht = basic_path + "/locations/pos_location_zht.jsonl"
file_path_neg_zht = basic_path + "/locations/neg_location_zht.jsonl"
map_path_pos_en = basic_path + "/locations/map_pos_en.html"
map_path_neg_en = basic_path + "/locations/map_neg_en.html"
map_path_reletive_en = basic_path + "/locations/map_reletive_en.html"
map_path_pos_zh = basic_path + "/locations/map_pos_zh.html"
map_path_neg_zh = basic_path + "/locations/map_neg_zh.html"
map_path_reletive_zh = basic_path + "/locations/map_reletive_zh.html"
map_path_pos_zhs = basic_path + "/locations/map_pos_zhs.html"
map_path_neg_zhs = basic_path + "/locations/map_neg_zhs.html"
map_path_reletive_zhs = basic_path + "/locations/map_reletive_zhs.html"
map_path_pos_zht = basic_path + "/locations/map_pos_zht.html"
map_path_neg_zht = basic_path + "/locations/map_neg_zht.html"
map_path_reletive_zht = basic_path + "/locations/map_reletive_zht.html"
min_valid_number_zh = 3
min_valid_number_zhst = 2
min_valid_number_en = 10

def drawmap(inputfile, outputfile, name, name_minor = ''):
    with open(inputfile, 'r') as fi:
        for line in jsonlines.Reader(fi):
            # print (line)
            countries = list(line.keys())
            numbers = list(line.values())
            # print ("numbers: ", numbers)
            MAX = max(numbers)
            MIN = min(numbers)
            numbers_modified = []
            for i in range(len(numbers)):
                numbers_modified.append(round((numbers[i] - MIN) * 100 / (MAX - MIN)))
            # print ("numbers: ", numbers)
            # print ("numbers_modified: ", numbers_modified)
            map0 = Map(name, name_minor, width=1400, height=700)
            map0.add(name, attr = countries, value = numbers, maptype="world", is_roam=True, is_map_symbol_show=False, is_visualmap=True, visual_text_color='#000')
            map0.add('modified to a 0-100 scale', attr = countries, value = numbers_modified, maptype="world", is_roam=True, is_map_symbol_show=False, is_visualmap=True, visual_text_color='#000')
            map0.render(path=outputfile)

def drawreletivemap(inputfile_pos, inputfile_neg, outputfile, min_valid_number, name, name_minor = ''):
    country_names = []
    reletive = {}
    divide = {}
    with open(inputfile_pos, 'r') as fp:
        for lp in jsonlines.Reader(fp):
            pos = lp
            for itemsp in lp:
                country_names.append(str(itemsp))
    with open(inputfile_neg, 'r') as fn:
        for ln in jsonlines.Reader(fn):
            neg = ln
            for itemsn in ln:
                if str(itemsn) not in country_names:
                    country_names.append(str(itemsn))
    for country_name in country_names:
        try:
            reletive[country_name] = pos[country_name] - neg[country_name]
            divide[country_name] = pos[country_name] / neg[country_name]
        except:
            try:
                reletive[country_name] = pos[country_name]
                if pos[country_name] > min_valid_number:
                    # divide[country_name] = 2
                    divide[country_name] = 0.99999995577455632789      # 需要绘制出归一化到0-100的图，和直接*50的图，为了程序简洁，后者在只有pos没有neg推文的情况下，
            except:                                                    # 可以与前者共享一个很奇怪的数，后面再直接赋值为100（原本也是赋值为2，后面和别的数一起*50）
                reletive[country_name] = - neg[country_name]
                if neg[country_name] > min_valid_number:
                    divide[country_name] = 0
    countries = list(reletive.keys())
    numbers = list(reletive.values())
    MAX = max(numbers)
    MIN = min(numbers)
    for i in range(len(numbers)):
        numbers[i] = round((numbers[i] - MIN) * 100 / (MAX - MIN))
    ZERO = round((0 - MIN) * 100 / (MAX - MIN))
    countries_division = list(divide.keys())
    numbers_division = list(divide.values())
    numbers_division_scaleto100 = list(divide.values())
    # for i in range(len(numbers_division)):
    #     numbers_division[i] = numbers_division[i] * 50
    MAX_d = max(numbers_division_scaleto100)
    MIN_d = min(numbers_division_scaleto100)
    assert numbers_division == numbers_division_scaleto100
    for i in range(len(numbers_division)):
        if numbers_division[i] == 0.99999995577455632789:
            numbers_division[i] = 100
            numbers_division_scaleto100[i] = 100
        else:
            numbers_division[i] = numbers_division[i] * 50
            numbers_division_scaleto100[i] = round((numbers_division_scaleto100[i] - MIN_d) * 100 / (MAX_d - MIN_d))
    ONE = round((1 - MIN_d) * 100 / (MAX_d - MIN_d))
    plan = Map(name, name_minor, width=1400, height=700)
    plan.add('minus，{}等效为中性情感'.format(ZERO), countries, numbers, maptype="world", is_roam=True, is_map_symbol_show=False, is_visualmap=True, visual_text_color='#000')
    plan.add('division，并x50，即50等效为中性情感', countries_division, numbers_division, maptype="world", is_roam=True, is_map_symbol_show=False, is_visualmap=True, visual_text_color='#000')
    plan.add('division，并归一化到0-100，{}等效为中性情感'.format(ONE), countries_division, numbers_division_scaleto100, maptype="world", is_roam=True, is_map_symbol_show=False, is_visualmap=True, visual_text_color='#000')
    plan.render(path=outputfile)

# drawmap(file_path_pos_en, map_path_pos_en, '英文推文积极情感分布地图')
# drawmap(file_path_neg_en, map_path_neg_en, '英文推文消极情感分布地图')
# drawreletivemap(file_path_pos_en, file_path_neg_en, map_path_reletive_en, '英文推文绝对情感分布地图', '积极情感值与消极情感值之差或之比，并转为0-100尺度')

drawmap(file_path_pos_en, map_path_pos_en, '英文推文积极情感分布地图')
drawmap(file_path_neg_en, map_path_neg_en, '英文推文消极情感分布地图')
drawreletivemap(file_path_pos_en, file_path_neg_en, map_path_reletive_en, min_valid_number_en, '英文推文绝对情感分布地图', '积极情感值与消极情感值之差或之比，并转为0-100尺度')

drawmap(file_path_pos_zh, map_path_pos_zh, '中文推文积极情感分布地图')
drawmap(file_path_neg_zh, map_path_neg_zh, '中文推文消极情感分布地图')
drawreletivemap(file_path_pos_zh, file_path_neg_zh, map_path_reletive_zh, min_valid_number_zh, '中文推文绝对情感分布地图', '积极情感值与消极情感值之差或之比，并转为0-100尺度')

drawmap(file_path_pos_zhs, map_path_pos_zhs, '简体中文推文积极情感分布地图')
drawmap(file_path_neg_zhs, map_path_neg_zhs, '简体中文推文消极情感分布地图')
drawreletivemap(file_path_pos_zhs, file_path_neg_zhs, map_path_reletive_zhs, min_valid_number_zhst, '简体中文推文绝对情感分布地图', '积极情感值与消极情感值之差或之比，并转为0-100尺度')

drawmap(file_path_pos_zht, map_path_pos_zht, '繁体中文推文积极情感分布地图')
drawmap(file_path_neg_zht, map_path_neg_zht, '繁体中文推文消极情感分布地图')
drawreletivemap(file_path_pos_zht, file_path_neg_zht, map_path_reletive_zht, min_valid_number_zhst, '繁体中文推文绝对情感分布地图', '积极情感值与消极情感值之差或之比，并转为0-100尺度')

geo = Geo("全国主要城市空气质量热力图", "data from pm2.5", title_color="#fff", title_pos="center", width=1200, height=600, background_color='#404a59')
geo.add("空气质量热力图", cities, air_quality, visual_range=[0, 25], type='heatmap',visual_text_color="#fff", symbol_size=15, is_visualmap=True, is_roam=False)
# geo.show_config()
geo.render(path="空气质量热力图.html") 
 
geo = Geo("全国主要城市空气质量评分", "data from pm2.5", title_color="#fff", title_pos="center", width=1200, height=600, background_color='#404a59')
# type="effectScatter", is_random=True, effect_scale=5  使点具有发散性
geo.add("空气质量评分", indexs, index_values, type="effectScatter", is_random=True, effect_scale=5, visual_range=[0, 5],visual_text_color="#fff", symbol_size=15, is_visualmap=True, is_roam=False)
# geo.show_config()
geo.render(path="空气质量评分.html") """
