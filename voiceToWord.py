import speech_recognition as sr
import pyttsx3
import pyaudio

r = sr.Recognizer()
test = sr.AudioFile("/Users/wenxinghua/Desktop/vedio/2.aiff")   #导入语音文件
with test as source:
    audio = r.record(source, offset=1, duration=100)
    type(audio)
    text = r.recognize_google(audio, language='zh-CN')
    print('我刚才说的内容是：', text)
#