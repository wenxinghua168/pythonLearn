import speech_recognition as sr
import pyttsx3
import re
import ssl
import urllib.request as ur
import urllib.parse as up
import json

# 智能语音识别
r = sr.Recognizer()
with sr.Microphone() as source:
    # 初始化文本朗读(各种语言)
    engine = pyttsx3.init()
    # 文字转化成语音
    engine.say("开启智能翻译，请开始：")
    #运行
    engine.runAndWait()
    # 读取 麦克风说的的音频内容，设置麦克风时间长度5s
    audio_data = r.record(source, duration=5)
    # 转化语音内容到文字，设置成中文
    word = r.recognize_google(audio_data, language='zh-CN')#zh-CN
    print(str(word))
    word = str(word)

    # 正确链接将链接中的
    url = 'https://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    # SSL证书的定义
    ssl._create_default_https_context = ssl._create_unverified_context
    # data数据传入的Form
    data = {
        'i': word,
        'doctype': 'json'
    }
    data_url = up.urlencode(data).encode('utf-8')
    request = ur.Request(url=url, data=data_url)
    response = ur.urlopen(request).read()
    ret = json.loads(response)
    translate = ret['translateResult'][0][0]['tgt']
    print('翻译结果为：%s' % translate)
    engine.say(translate)
    engine.runAndWait()