import pyttsx3
import urllib.request
import re
import os
import urllib
import ssl
import sys
#定义爬虫类
class readBook:
    #根据给定的网址来获取网页详细信息，得到的html就是网页的源代码
    def getHtml(slef,url):
        # 设置ssl 证书
        ssl._create_default_https_context = ssl._create_unverified_context
        # 请求打开网页链接
        page = urllib.request.urlopen(url)
        # 获取网页内容 设置成UTF-8格式
        html = page.read().decode('UTF-8')
        # 返回 取得网页内容
        return html
    #书本信息 内容在取得
    def getContext(slef,html):
        # 匹配 小说章节名
        regTitle =r'title_txtbox">(.*)</div>'
        # 匹配查找所有内容
        reg =r'"acticleBody".+?.\n.+?(<p>.+?</p>).\n.+?.*</div>'
        # 匹配查找各个段落（行）
        regCont =r'<p>(.+?)</p>'
        # 匹配查找下一章节URL地址
        regNextPage =r'href="(.+?.html)".*class="nextchapter"'
        matchTitle = re.compile(regTitle)
        matchContent = re.compile(reg)
        matchCont = re.compile(regCont)
        matchNextPage = re.compile(regNextPage)
        # 内容
        contentList = matchContent.findall(html, re.M)
        # 标题
        title = matchTitle.findall(html)
        # 下一章节
        nextpageURL = matchNextPage.findall(html)

        # 启动语音
        engine = pyttsx3.init()
        print(title)
        # 读出章节名字
        engine.say(str(title))
        engine.runAndWait()
        # 分段落（行）放入List集合中
        contList = matchCont.findall(contentList.__getitem__(0))
        # for cont in contList:
        # 读出没段落（行）的内容
        engine.say(str(contList))
        engine.runAndWait()
        return nextpageURL
# ✨✨✨✨✨✨✨✨✨✨✨懒人听书程序开始✨✨✨✨✨✨✨✨✨✨✨✨
# 懒人听书启动
readBook = readBook()
# 想要听说的小说页面的网址
url = "http://book.zongheng.com/chapter/189169/3431701.html"
# 取得当前页面所有信息
html = readBook.getHtml(url)
# 取下一章节网址
nextPage = readBook.getContext(html)
# 比如 循环收听 前50 章节的内容
pagNum = 1
while pagNum < 50:
    pagNum = pagNum+1
    # 取得下一章节URL
    nextHtml = readBook.getHtml(nextPage.__getitem__(0))
    # 取得下一章节的内容
    nextPage = readBook.getContext(nextHtml)