import os
import shutil
import jsonlines
import json

basic_path = os.getcwd()
# file_path_pos_en = basic_path + "/result/pos_location_en.jsonl"
# file_path_neg_en = basic_path + "/result/neg_location_en.jsonl"
file_path_pos_en = basic_path + "/locations/pos_selected_location_en.jsonl"
file_path_neg_en = basic_path + "/locations/neg_selected_location_en.jsonl"
file_path_pos_zh = basic_path + "/result/pos_location_zh.jsonl"
file_path_neg_zh = basic_path + "/result/neg_location_zh.jsonl"
file_path_pos_zhs = basic_path + "/result/pos_location_zhs.jsonl"
file_path_neg_zhs = basic_path + "/result/neg_location_zhs.jsonl"
file_path_pos_zht = basic_path + "/result/pos_location_zht.jsonl"
file_path_neg_zht = basic_path + "/result/neg_location_zht.jsonl"
file_path_correspondence = basic_path + '/locations_correspondence.jsonl'
file_path_target_pos_en = basic_path + "/locations/pos_location_en.jsonl"
file_path_target_neg_en = basic_path + "/locations/neg_location_en.jsonl"
file_path_target_pos_zh = basic_path + "/locations/pos_location_zh.jsonl"
file_path_target_neg_zh = basic_path + "/locations/neg_location_zh.jsonl"
file_path_target_pos_zhs = basic_path + "/locations/pos_location_zhs.jsonl"
file_path_target_neg_zhs = basic_path + "/locations/neg_location_zhs.jsonl"
file_path_target_pos_zht = basic_path + "/locations/pos_location_zht.jsonl"
file_path_target_neg_zht = basic_path + "/locations/neg_location_zht.jsonl"
file_path_target_knownlocations = basic_path + "/locations/knownlocations.txt"

# knownlocations = {'China': {'Mainland': 0, 'Hong Kong': 0, 'Macau': 0, "Taiwan": 0}, 'United States': 0, "Russia": 0, "United Kingdom": 0, "France": 0, "Germany": 0, 
#             "Japan": 0, "Korea": 0, "Italy": 0, "Canada": 0, "Australia": 0, "New Zealand": 0, "Brazil": 0, "Vietnam": 0, "Malasia": 0, "Thailand": 0}

knownlocations = ['China', 'United States', "Russia", "United Kingdom", "France", "Germany", "Japan", "Korea", "Italy", "Canada", "Australia", "New Zealand", "Brazil", 
                "Vietnam", "Malaysia", "Thailand", "Pakistan", "India", "United Arab Emirates", "Madagascar", "South Africa", "Paraguay", "Indonesia", "Poland", 
                "Denmark", "Nigeria", "Botswana", "Chile", "Uganda", "Nepal", "Belgium", "Saudi Arabia", "Philippines", "Tanzania", "Spain", "Niger", "Somalia", "Norway", 
                "Ecuador", "Sri Lanka", "Venezuela", "Dominican Rep.", "Ukraine", "Serbia", "Ireland", "Singapore", "Netherlands", "Turkey", "Malawi", "Peru", "Armenia", 
                "Bulgaria", "Malta", "El Salvador", "Switzerland", "Portugal", "Mexico", "Lebanon", "Finland", "Cyprus", "Lithuania", "Macedonia", "Iraq", "Afghanistan", 
                "Ghana", "Bosnia and Herz.", "Guam", "Uruguay", "Trinidad and Tobago", "Uzbekistan", "Argentina", "C\u00f4te d'Ivoire", "Bahrain", "Jordan", "Kuwait", 
                "Panama", "Czech Rep.", "Zimbabwe", "Luxembourg", "Croatia", "NotACountry"]

""" if os.path.exists(basic_path + "/locations"):
    shutil.rmtree(basic_path + "/locations", True)
    print ('{} deleted'.format(basic_path + "/locations"))
os.mkdir(basic_path + "/locations") """

def judge(name):
    Text = {"1":"\n" + name + "? ", "2": "\n输入非允许项！", "3": "\n输入内容不在已有库中，是否确认？ y or n? "}
    try:
        judge = input(Text["1"])
        while judge not in knownlocations:
            judgeagain = input(Text["3"])
            if judgeagain == 'y':
                knownlocations.append(judge)
                break
            elif judgeagain == 'n':
                judge = input(Text["1"])
    except:
        judge = input(Text["2"])
        while judge not in knownlocations:
            judgeagain = input(Text["3"])
            if judgeagain == 'y':
                knownlocations.append(judge)
                break
            elif judgeagain == 'n':
                judge = input(Text["1"])
    return judge

def decidelocations(inputfile, outputfile):
    print ('\n' + inputfile + '\n')
    location = {}
    with open(inputfile, 'r') as fi:
        for line in jsonlines.Reader(fi):
            for item in line:
                with open(file_path_correspondence, 'r', encoding='UTF-8') as fc:
                    isFound = 0
                    for fclines in jsonlines.Reader(fc):
                        if fclines['name'] in str(item):
                            try:
                                location[fclines['location']] += line[item]
                            except:
                                location[fclines['location']] = line[item]
                            isFound = 1
                            break
                if isFound == 0:
                    locationname = judge(str(item))
                    try:
                        addname = input('保存为？')
                        if addname == ' ':
                            print("按原样保存")
                            new = {'name': str(item), 'location': locationname}
                        else:
                            new = {'name': str(addname), 'location': locationname}
                    except:
                        print("按原样保存")
                        new = {'name': str(item), 'location': locationname}
                    with open(file_path_correspondence, 'a') as fca:
                        fca.write(json.dumps(new)+'\n')
                    try:
                        location[locationname] += line[item]
                    except:
                        location[locationname] = line[item]
    with open(outputfile, 'a') as fo:
        fo.write(json.dumps(location))

decidelocations(file_path_pos_zht, file_path_target_pos_zht)
decidelocations(file_path_neg_zht, file_path_target_neg_zht)
decidelocations(file_path_pos_zhs, file_path_target_pos_zhs)
decidelocations(file_path_neg_zhs, file_path_target_neg_zhs)
decidelocations(file_path_pos_zh, file_path_target_pos_zh)
decidelocations(file_path_neg_zh, file_path_target_neg_zh)
decidelocations(file_path_pos_en, file_path_target_pos_en)
decidelocations(file_path_neg_en, file_path_target_neg_en)

with open(file_path_target_knownlocations,"w", encoding = 'UTF-8') as f:
    f.write(str(knownlocations))

# Brasil, Sweden, Malasia, Myanmar