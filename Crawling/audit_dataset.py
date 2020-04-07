from tqdm import tqdm


def get_invalid_character(dicts, data):
    invalid_data = []
    for character in data:
        if character == ' ' or dicts[character] < 120:
            invalid_data.append(character)
    if len(invalid_data) > 0:
        return invalid_data
    else:
        return None


def audit_classes(dictionary_path):
    classes = count_classes(dictionary_path)
    with open(dictionary_path, 'r') as f:
        with open('/home/hjpark/Workspace/OCR/data/dict/kr_audit.txt', 'w') as target_f:
            while True:
                line = f.readline()
                if not line: break
                invalid_character = get_invalid_character(classes, line.strip('\n'))
                if invalid_character is not None:
                    target_f.write(''.join(invalid_character) + '\t' + line)


def remove_space():
    samples = {}
    with open('/home/hjpark/Workspace/OCR/data/dict/kr.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line: break
            for item in line.strip().split():
                samples[item] = 1
    with open('/home/hjpark/Workspace/OCR/data/dict/kr_removed.txt', 'w') as f:
        for key in samples.keys():
            f.write(key + '\n')


def count_classes(dictionary_path):
    classes = {}
    with open(dictionary_path, 'r') as f:
        while True:
            line = f.readline()
            if not line: break
            for ch in line.strip('\n'):
                if classes.get(ch) is not None:
                    classes[ch] += 1
                else:
                    classes[ch] = 1
    return classes


def print_classes_status(classes, out_path):
    with open(out_path, 'w') as f:
        for key, value in sorted(classes.items(), key=(lambda x: x[1])):
            f.write(key + '\t' + str(value) + '\n')


def write_label_file(dictionary, out_path):
    count = 0
    sparse_file = open(out_path.replace('label', 'black'), 'w')
    with open(out_path, 'w') as f:
        f.write(str(count) + '\t' + '<UNK>' + '\n')
        count += 1
        for key in sorted(dictionary.keys()):
            if dictionary[key] > 1200:
                f.write(str(count) + '\t' + key + '\n') # ID\tTEXT 조합으로 저장
                count += 1
            else:
                sparse_file.write(key + '\n')



if __name__ == '__main__':
    dict_path = '/home/hjpark/Workspace/OCR/data/dict/kr.txt'
    out_path = '/home/hjpark/Workspace/OCR/data/dict/kr_status.txt'
    label_path = '/home/hjpark/Workspace/OCR/data/dict/kr_label.txt'
    classes = count_classes(dict_path)
    # print_classes_status(classes, out_path)
    # 1200 번 이하로 등장하는 문자는 모두 <UNK>로 처리한다.
    write_label_file(classes, label_path)








