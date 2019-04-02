import requests
import os
import time
from itertools import product


def spider():
    page = 0

    temp = list(product("abcdef", repeat=6))

    search_word = [''.join(i) for i in temp]
    word_count = 0
    error_count = 0
    while True:
        try:
                if word_count == len(search_word):
                    break

                if error_count > 5:
                    word_count += 1

                url = 'https://www.google.co.kr/search?q=filetype:doc+{}&ei=SmCbXIL4CpT7wAO4vY_ACg&start={}&sa=N&ved=0ahUKEwiCxY_QnaLhAhWUPXAKHbjeA6gQ8tMDCIUB&cshid=1553686629088338&biw=1272&bih=594'.format(search_word[word_count], page)
                headers = {
                    'User-Agent': 'My User Agent 1.0',
                    'From': 'youremail@domain.com'  # This is another valid field
                }
                source_code = requests.get(url, headers=headers, timeout=5)
                if source_code.status_code == 503:
                    print("503")
                    word_count += 1
                    print("현재 wordcount: ", word_count, "현재 doc str:", search_word[word_count], url)
                    continue

                temp = source_code.text
                index_list = []
                real_url = []
                start = 0

                if temp.find('<a href="/url?q=') == -1:
                    word_count += 1
                    page = 0
                    continue

                while True:
                    start = temp.find('<a href="/url?q=', start+1)
                    if start == -1:
                        break
                    index_list.append(start)

                for i in index_list:
                    real_url.append(temp[i+16:i+100].split('.doc')[0]+'.doc')

                for i in range(0, len(real_url)):
                    try:
                        response = requests.get(real_url[i], timeout=5)
                        if response.status_code == 200:
                            file_name = '{}_{}_'.format(search_word[word_count], page) + str(i) + '.doc'
                            start_time = time.time()
                            flag = False
                            save_path = os.path.join('/mnt/hgfs/doc', file_name)
                            handle = open(save_path, "wb")

                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:  # filter out keep-alive new chunks
                                    handle.write(chunk)
                                if time.time() - start_time > 360:
                                    print(file_name, "time_out")
                                    flag = True
                                    break

                            handle.close()

                            if os.path.getsize(save_path) < 10000 or flag is True:
                                os.remove(save_path)
                                print(file_name, "download remove")
                            else:
                                print(file_name, "download finished")
                                error_count = 0

                    except Exception as ep:
                        print("second except", ep)

                page += 10

        except Exception as ep:
            print("first", ep)
            error_count += 1
            page += 10


if __name__ == '__main__':
    spider()
