import pathlib
import random
import requests
import time
import json
import pandas

# 模拟浏览器参数

def get_user_agent():

    path = pathlib.Path("browsers.json")

    if not path.exists():

        url = 'http://fake-useragent.herokuapp.com/browsers/0.1.8'

        response = requests.get(url)

    with open("browsers.json", "w") as f:

        json.dump(response.text, f)

    with open("browsers.json", "r") as f:

    # load操作文件，loads将字符串转为json

        browsers_data = json.loads(json.load(f))["browsers"]

        browser_type = ['chrome', 'opera', 'firefox', 'internetexplorer', 'safari'][random.randint(0, 4)]

        length = len(browsers_data[browser_type])

        user_agent = browsers_data[browser_type][random.randint(0, length - 1)]

    return user_agent

# 封装请求参数(url，user-agent，proxy)

def get_request_param():

    current_time = int(time.time())

    url = "https://www.toutiao.com/api/pc/feed/?" \

    "max_behot_time=" + str(current_time) + "&category=__all__&utm_source=toutiao&widen=1&tadrequire=true&as=A1B53D2663BEC17" \

    "&cp=5D632E0C91A7DE1&_signature=0pxnghAZkAg82jjJUf.eiNKcZ5"

    proxies = {
    "url": "http:120.76.191.177:8118"

    }

    headers = {
    "user-agent": get_user_agent()

    }

    return url, headers, proxies

# 爬取头条新闻

def get_news():

    url, headers, proxies = get_request_param()

    response = requests.get(url, headers=headers, proxies=proxies)

    global response_json
    response_json = json.loads(response.text)

    if response_json['message'] == 'error':
        get_news()
    return response_json

# 将爬取到的信息写入文件中

def write_to_file(news_text):
    print(news_text)
#
# news = news_text['data']
#
# for i in range(len(news)):
#
# with open("news_json", "a+") as f:
#
# json.dump(news[i], f, ensure_ascii=False)
#
# f.write("\n")
#
# write_to_file(get_news())
#
# df = pandas.DataFrame(pandas.read_json('news_json', lines=True))
#
# df.to_excel('toutiao.xlsx')