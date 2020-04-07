import ijson 
from collections import OrderedDict 

# with open ('./trdg/dicts/namuwiki190312/namuwiki_20190312.json') as json_file: 

#     json_data = ijson.items(json_file) 
#     for json_object in json_data : 
#         print (json_object)
#         break
class TopNDict():
    def __init__(self, max_item):
        self.dict = OrderedDict()
        self.max_item = max_item
        self.count = 0 
    
    def push(self, key):
        if self.dict.get(key) is None: 
            if self.count < self.max_item :
                self.dict[key] = 1                 
            else:
                self.pop() 
                self.dict[key] = 1
            self.count +=1 
        else:
            self.dict[key] +=1 
    
    def pop(self):
        min_value = 10240 
        popped = False
        for key, value in self.dict.items():
            min_value = min(min_value, value)
        
        for key, value in self.dict.items():
            if value == min_value :
                del self.dict [key]
                popped = True
                break         
        if popped == False : 
            raise Exception('pop {} is failed '.format(min_value))
        self.count -= 1 

    def print(self):
        for key, value in sorted(self.dict.items(), key=lambda item: item[1]):
            print ("key:{}, value:{}".format(key,value))
        

namu_dict = TopNDict(1000) 

loop_count = 0 

blacklist = {}
with open('/home/hjpark/Workspace/OCR/data/dict/kr_black.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        blacklist[line.strip()] = 1


whitelist = {}
with open('/home/hjpark/Workspace/OCR/data/dict/kr_label.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        character = line.strip().split()[1]
        whitelist[character] = 1

out_file = open('namu_blacklist.txt', 'w')
with open('/home/hjpark/Workspace/OCR/data/namuwiki_20190312.json') as json_file:
    # parser = ijson.parse(json_file)
    objects = ijson.items(json_file, 'item.text')
    for obj in objects:
        words = obj.replace('[[', '').replace(']]', '').replace('==', '').replace('--', '').replace('...', '').replace("'''", '').replace('\\\\','').split()
        # for word in words : 
        #     namu_dict.push(word)
        # loop_count += 1 
        # if loop_count > 1000:
        #     break
        for word in words:
            found = False
            for character in word:
                if whitelist.get(character) is None and blacklist.get(character) is not None:
                    found = True
                elif whitelist.get(character) is None and blacklist.get(character) is None :
                    found = False
                    break
            if found:
                out_file.write(word + '\n')
