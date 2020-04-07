import urllib.request as request
import json
import time


def get_data(page_id, out_file):
    url = "https://koreanname.me/api/rank/2008/2020/{}".format(page_id)
    req = request.Request(url=url, method='GET')
    count = 0
    with request.urlopen(req) as f:
        results = json.loads(f.read().decode('utf-8'))
        for female_obj in results['female']:
            out_file.write(female_obj['name'] + '\n')
            count +=1

        for male_obj in results['male']:
            out_file.write(male_obj['name'] + '\n')
            count += 1
    return count


if __name__ == "__main__":
    with open('data/name.txt', 'w') as f:
        for i in range(1, 1000):
            count = get_data(i, f)
            print('{} has {} data'.format(i, count))
            time.sleep(5)
