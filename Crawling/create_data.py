import os
import urllib.request as request
import base64
from bs4 import BeautifulSoup
from urllib import parse
from Crawling.util import pickle_load
from Crawling.util import pickle_save
import time

RESULT_PATH = "./Crawling/result/"


def generate_full_name(last_names, family_names):
    name_dict = {}
    with open('./Crawling/result/full_name.txt', 'w') as f:
        for family_name in family_names:
            for last_name in last_names:
                name = family_name + last_name
                f.write( name + '\n')
                if name_dict.get(name) is None:
                    name_dict[name] = 1
                else:
                    print('duplicated name {}'.format(name))


def get_english_name(name):
    results = []
    url = "https://dict.naver.com/name-to-roman/translation/?query={}&y=0&where=name".format(parse.quote(name))
    req = request.Request(url=url, method='GET')
    with request.urlopen(req) as f:
        html = '\n '.join([ l.decode('utf-8') for l in f.readlines()])
        bs = BeautifulSoup(html,'html.parser')
        for obj in bs.find_all("td", {"class":"cell_engname"}):
            results.append(obj.text)
    return results


def get_name_character_class():
    characters = {}
    cache_path = os.path.join(RESULT_PATH, 'get_name_character_class.pickle')
    if os.path.exists(cache_path) :
        characters = pickle_load(cache_path)
        return characters

    with open('./Crawling/result/full_name.txt', 'r') as f:
        while True:
            name = f.readline()
            if not name: break
            for ch in name:
                characters[ch] = []

    pickle_save(cache_path, characters)
    return characters


def get_kor2eng_translation():
    cache_path = os.path.join(RESULT_PATH, 'get_kor2eng_translation.pickle')
    if os.path.exists(cache_path):
        return pickle_load(cache_path)

    kor_name_characters = get_name_character_class()
    for ch in kor_name_characters.keys():
        eng_characters = get_english_name(ch)
        time.sleep(1)
        kor_name_characters[ch].append(eng_characters)

    pickle_save(cache_path, kor_name_characters)
    return kor_name_characters


# 영어 이름은 성과 이름을 뜨어서 사용하므로
# 성과 이름을 따로 따로 만들어야 한다.
def generate_eng_familyname(kor2eng):
    eng_family_name_f = open('./Crawling/result/eng_family_name.txt', 'w')
    with open('./Crawling/data/familyname.csv', 'r') as f:
        while True:
            name = f.readline()
            if not name: break
            else:
                name = name.strip()
            for kor_ch in name:
                for eng_ch in kor2eng[kor_ch][0]:
                    eng_ch = eng_ch.strip().upper()
                    eng_family_name_f.write(eng_ch + '\n')

def generate_eng_name(kor2eng):
    name_dict = {}
    eng_name_f = open('./Crawling/result/eng_name.txt', 'w')
    with open('./Crawling/data/name.txt', 'r') as f:
        while True:
            name = f.readline()
            if not name: break
            else:
                name = name.strip()
            if name_dict.get(name) is not None:
                continue
            else:
                name_dict[name] = 1
            eng_names = ['']
            for kor_ch in name:
                new_eng_names = []
                for eng_ch in kor2eng[kor_ch][0]:
                    eng_ch = eng_ch.strip().upper()
                    for eng_name in eng_names:
                        new_eng_names.append(eng_name + eng_ch)
                        if eng_name is not '':
                            new_eng_names.append(eng_name + '-' + eng_ch)

                eng_names = new_eng_names
            for eng_name in eng_names:
                eng_name_f.write(eng_name + '\n')


def generate_year(file):
    for i in range(1800, 2020):
        file.write(str(i) + '\n')


def generate_month(file):
    file.write('Jan' + '\n')
    file.write('Feb' + '\n')
    file.write('Mar' + '\n')
    file.write('Apr' + '\n')
    file.write('May' + '\n')
    file.write('Jun' + '\n')
    file.write('Jul' + '\n')
    file.write('Aug' + '\n')
    file.write('Sep' + '\n')
    file.write('Oct' + '\n')
    file.write('Nov' + '\n')
    file.write('Dec' + '\n')

    for i in range(0, 12):
        file.write('.' + str(i) + '\n')
        file.write('.' + format(i, '02') + '\n')


def generate_day(out_file):
    for i in range(0, 32):
        out_file.write(str(i) + '\n')
        out_file.write('.' + str(i) + '\n')
        out_file.write(format(i, '02') + '\n')
        out_file.write('.' + format(i, '02') + '\n')


def generate_eng_date():
    # 2016.3.2 style 16 MAY 2017 style 2가지가 있다.
    # 그런데 실제로 각 digit size에 space가 있으므로 2016 .3 .2 16 MAY 2017 로 각각 학습을 시켜야 한다.
    date_file = open('./Crawling/result/date.txt', 'w')
    generate_year(date_file)
    generate_month(date_file)
    generate_day(date_file)



if __name__ == "__main__":
    family_name_dict = {}
    with open('./Crawling/data/familyname.csv', 'r') as family_name_file:
        for line in family_name_file.readlines():
            family_name_dict[line.strip()] = 1
    last_name_dict = {}
    with open('./Crawling/data/name.txt', 'r') as name_file:
        for line in name_file.readlines():
            last_name_dict[line.strip()] = 1

    # generate_full_name(last_name_dict, family_name_dict)
    # get_kor2eng = get_kor2eng_translation()
    # generate_eng_name(get_kor2eng)
    # generate_eng_familyname(get_kor2eng)
    generate_eng_date()



