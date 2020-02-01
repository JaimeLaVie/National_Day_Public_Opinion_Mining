import os
import jsonlines
import pygal
import pygal_maps_world.maps
from pygal.maps.world import COUNTRIES
# import json

basic_path = os.getcwd()
file_path_pos_en = basic_path + "/locations/pos_location_en.jsonl"
file_path_neg_en = basic_path + "/locations/neg_location_en.jsonl"
file_path_pos_zh = basic_path + "/locations/pos_location_zh.jsonl"
file_path_neg_zh = basic_path + "/locations/neg_location_zh.jsonl"
file_path_pos_zhs = basic_path + "/locations/pos_location_zhs.jsonl"
file_path_neg_zhs = basic_path + "/locations/neg_location_zhs.jsonl"
file_path_pos_zht = basic_path + "/locations/pos_location_zht.jsonl"
file_path_neg_zht = basic_path + "/locations/neg_location_zht.jsonl"
jpgmap_path_pos_en = basic_path + "/locations/map_pos_en.svg"
jpgmap_path_neg_en = basic_path + "/locations/map_neg_en.svg"
jpgmap_path_reletive_en = basic_path + "/locations/map_reletive_en.svg"
jpgmap_path_pos_zh = basic_path + "/locations/map_pos_zh.svg"
jpgmap_path_neg_zh = basic_path + "/locations/map_neg_zh.svg"
jpgmap_path_reletive_zh = basic_path + "/locations/map_reletive_zh.svg"
jpgmap_path_pos_zhs = basic_path + "/locations/map_pos_zhs.svg"
jpgmap_path_neg_zhs = basic_path + "/locations/map_neg_zhs.svg"
jpgmap_path_reletive_zhs = basic_path + "/locations/map_reletive_zhs.svg"
jpgmap_path_pos_zht = basic_path + "/locations/map_pos_zht.svg"
jpgmap_path_neg_zht = basic_path + "/locations/map_neg_zht.svg"
jpgmap_path_reletive_zht = basic_path + "/locations/map_reletive_zht.svg"
min_valid_number_zh = 3
min_valid_number_zhst = 2
min_valid_number_en = 10
country_codes = {"Russia": "ru", "Côte d'Ivoire": "ci", "Dominican Rep.": "do", "Venezuela": "ve", "Tanzania": "tz", "Vietnam": "vn", "Macedonia": "mk", "Korea": "kr",
                "Bosnia and Herz.": "ba", "Palestine": "ps", "New Caledonia": "fr", "Czech Rep.": "cz", "Iran": "ir", "Hrvatska": "hr"}

def get_country_code(country_name):
    #根据指定的国家，返回Pygal使用的两个字母的国别码
    for code, name in COUNTRIES.items():
        if name == country_name:
            return code
    for name in country_codes:
        if name == country_name:
            return country_codes[name]
    print (country_name)
    return None

def TransformCountryCode(inputjson):
    outputjson = {}
    for items in inputjson:
        countryCode = get_country_code(items)
        outputjson[countryCode] = inputjson[items]
    outputjson["tw"] = outputjson["cn"]
    return outputjson

def classification(inputjson, isDivide):
    numbers = list(inputjson.values())
    if isDivide == True:
        n9 = 2
        n7 = 1.5
        n5 = 1
        n3 = 0.667
        n1 = 0.333
    else:
        MAX = max(numbers)
        MIN = min(numbers)
        n9 = round((MAX - MIN) * 0.9) + MIN
        n7 = round((MAX - MIN) * 0.7) + MIN
        n5 = round((MAX - MIN) * 0.5) + MIN
        n3 = round((MAX - MIN) * 0.3) + MIN
        n1 = round((MAX - MIN) * 0.1) + MIN
    out90, out79, out57, out35, out13, out01 = {}, {}, {}, {}, {}, {}
    for councode,num in inputjson.items():
        if num >= n9:
            out90[councode] = num
        elif num >= n7:
            out79[councode] = num
        elif num >= n5:
            out57[councode] = num
        elif num >= n3:
            out35[councode] = num
        elif num >= n1:
            out13[councode] = num
        else:
            out01[councode] = num
    return out90, out79, out57, out35, out13, out01, n9, n7, n5, n3, n1


def drawmap(inputfile, outputfile, name):
    with open(inputfile, 'r') as fi:
        for line in jsonlines.Reader(fi):
            # print (line)
            """ countries = list(line.keys())
            numbers = list(line.values()) """
            # print ("numbers: ", numbers)
            newline = TransformCountryCode(line)
            country90, country79, country57, country35, country13, country01, n9, n7, n5, n3, n1 = classification(newline, False)
            wm_style=pygal.style.RotateStyle('#D35400',base_style=pygal.style.LightColorizedStyle)
            wm = pygal_maps_world.maps.World(style = wm_style)
            wm.title = name
            wm.add('>' + str(n9), country90)
            wm.add(str(n7) + '-' + str(n9), country79)
            wm.add(str(n5) + '-' + str(n7), country57)
            wm.add(str(n3) + '-' + str(n5), country35)
            wm.add(str(n1) + '-' + str(n3), country13)
            wm.add('<' + str(n1), country01)
            wm.render_to_file(outputfile)

def drawreletivemap(inputfile_pos, inputfile_neg, outputfile, min_valid_number, name):
    country_names = []
    # reletive = {}
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
            # reletive[country_name] = pos[country_name] - neg[country_name]
            divide[country_name] = pos[country_name] / neg[country_name]
        except:
            try:
                # reletive[country_name] = pos[country_name]
                if pos[country_name] > min_valid_number:
                    # divide[country_name] = 2
                    divide[country_name] = pos[country_name]
            except:                                            
                # reletive[country_name] = - neg[country_name]
                if neg[country_name] > min_valid_number:
                    divide[country_name] = 0
    # countries = list(reletive.keys())
    # numbers = list(reletive.values())
    # MAX = max(numbers)
    # MIN = min(numbers)
    # for i in range(len(numbers)):
    #     numbers[i] = round((numbers[i] - MIN) * 100 / (MAX - MIN))
    # ZERO = round((0 - MIN) * 100 / (MAX - MIN))
    # countries_division = list(divide.keys())
    # numbers_division = list(divide.values())
    newline = TransformCountryCode(divide)
    country90, country79, country57, country35, country13, country01, n9, n7, n5, n3, n1 = classification(newline, True)
    wm_style=pygal.style.RotateStyle('#D35400',base_style=pygal.style.LightColorizedStyle)
    wm = pygal_maps_world.maps.World(style = wm_style)
    wm.title = name
    wm.add('>' + str(n9), country90)
    wm.add(str(n7) + '-' + str(n9), country79)
    wm.add(str(n5) + '-' + str(n7), country57)
    wm.add(str(n3) + '-' + str(n5), country35)
    wm.add(str(n1) + '-' + str(n3), country13)
    wm.add('<' + str(n1), country01)
    wm.render_to_file(outputfile)
    # numbers_division_scaleto100 = list(divide.values())
    # for i in range(len(numbers_division)):
    #     numbers_division[i] = numbers_division[i] * 50
    # MAX_d = max(numbers_division_scaleto100)
    # MIN_d = min(numbers_division_scaleto100)
    # assert numbers_division == numbers_division_scaleto100
    # for i in range(len(numbers_division)):
    #     if numbers_division[i] == 0.99999995577455632789:
    #         numbers_division[i] = 100
    #         numbers_division_scaleto100[i] = 100
    #     else:
    #         numbers_division[i] = numbers_division[i] * 50
    #         numbers_division_scaleto100[i] = round((numbers_division_scaleto100[i] - MIN_d) * 100 / (MAX_d - MIN_d))
    # ONE = round((1 - MIN_d) * 100 / (MAX_d - MIN_d))
    # plan = Map(name, name_minor, width=1400, height=700)
    # plan.add('minus，{}等效为中性情感'.format(ZERO), countries, numbers, maptype="world", is_roam=True, is_map_symbol_show=False, is_visualmap=True, visual_text_color='#000')
    # plan.add('division，并x50，即50等效为中性情感', countries_division, numbers_division, maptype="world", is_roam=True, is_map_symbol_show=False, is_visualmap=True, visual_text_color='#000')
    # plan.add('division，并归一化到0-100，{}等效为中性情感'.format(ONE), countries_division, numbers_division_scaleto100, maptype="world", is_roam=True, is_map_symbol_show=False, is_visualmap=True, visual_text_color='#000')
    # plan.render(path=outputfile)

drawmap(file_path_pos_en, jpgmap_path_pos_en, '英文推文积极情感分布地图')
drawmap(file_path_neg_en, jpgmap_path_neg_en, '英文推文消极情感分布地图')
drawreletivemap(file_path_pos_en, file_path_neg_en, jpgmap_path_reletive_en, min_valid_number_en, '英文推文绝对情感分布地图')

drawmap(file_path_pos_zh, jpgmap_path_pos_zh, '中文推文积极情感分布地图')
drawmap(file_path_neg_zh, jpgmap_path_neg_zh, '中文推文消极情感分布地图')
drawreletivemap(file_path_pos_zh, file_path_neg_zh, jpgmap_path_reletive_zh, min_valid_number_zh, '中文推文绝对情感分布地图')

drawmap(file_path_pos_zhs, jpgmap_path_pos_zhs, '简体中文推文积极情感分布地图')
drawmap(file_path_neg_zhs, jpgmap_path_neg_zhs, '简体中文推文消极情感分布地图')
drawreletivemap(file_path_pos_zhs, file_path_neg_zhs, jpgmap_path_reletive_zhs, min_valid_number_zhst, '简体中文推文绝对情感分布地图')

drawmap(file_path_pos_zht, jpgmap_path_pos_zht, '繁体中文推文积极情感分布地图')
drawmap(file_path_neg_zht, jpgmap_path_neg_zht, '繁体中文推文消极情感分布地图')
drawreletivemap(file_path_pos_zht, file_path_neg_zht, jpgmap_path_reletive_zht, min_valid_number_zhst, '繁体中文推文绝对情感分布地图')
