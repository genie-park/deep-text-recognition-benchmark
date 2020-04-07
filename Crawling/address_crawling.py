import os
import glob
import pandas as pd
root_path = './Crawling/address/202002_건물DB_전체분/*.txt'

def get_address_words(path, cache):
    with open(path, 'r', encoding='ms949') as f:
        while True:
            line = f.readline()
            if not line:
                break
            items = [s.replace("'", "") for s in line.strip().split('|')]
            for item in items:
                for word in item.split():
                    if not item.isdigit():
                        if cache.get(word) is None:
                            cache[word] = 1
                        else:
                            cache[word] += 1
    return cache


cache = {}
for path in glob.glob(root_path):
    print(path)
    address = get_address_words(path, cache)

with open('./Crawling/result/address.txt', 'w') as f:
    for key in cache.keys():
        f.write(key + '\n')

# with open('./Crawling/result/building_detail_name.txt', 'w') as f:
#     for building_detail in buildings_detail.keys():
#         f.write(building_detail + '\n')


