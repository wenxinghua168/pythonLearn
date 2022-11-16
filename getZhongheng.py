import pyttsx3
import urllib.request
import re
import os
import urllib
import ssl
import time
import traceback
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

    # 网站首页检索书名
    def getSerachBookURL(slef,html):
        # 匹配 查找小说URL
        regBookURL = r'<a href="(.+?\.html)".*书籍详情</a>'
        # .\n表示换行符号
        matchBookURL = re.compile(regBookURL)
        searchBookURL = matchBookURL.findall(html, re.M).__getitem__(0)
        return searchBookURL

    # 检索得到书名的URL再次取得 阅读第一章节的URL
    def getSerachBookURL2(slef,html,bookName):
        # 匹配 查找小说URL
        regBookURL = r'href="(.+?\.html)".*开始阅读'
        matchBookURL = re.compile(regBookURL)
        searchBookURL = matchBookURL.findall(html, re.M).__getitem__(0)

        # author
        regAuthor =r'class="au-name">.+?>(.*)</a>'
        matchAuthor = re.compile(regAuthor)
        author = matchAuthor.findall(html, re.M).__getitem__(0)
        # type
        regtype = r'首页.+?">(.*)</a>'
        matchtype = re.compile(regtype)
        type = matchtype.findall(html, re.M).__getitem__(0)
        regSummary = r'<div class="book-dec Jbook-dec hide">.\n.+?.+?<p>(.*)</p>'
        matchSummary = re.compile(regSummary)
        summary = matchSummary.findall(html)

        # 初始化文本朗读(各种语言)
        engine = pyttsx3.init()
        # 文字转化成语音
        print(bookName, '作者:', author)
        engine.say(str(bookName + ',作者'+author))
        # 运行
        engine.runAndWait()
        return searchBookURL

    #书本信息 内容在取得
    def getContext(slef,html, bookName):
        ssl._create_default_https_context = ssl._create_unverified_context
        # 匹配 小说名字
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

        # 读出章节名字
        engine = pyttsx3.init()
        print(title)
        engine.say(str(title))
        engine.runAndWait()
        # 分段落（行）放入List集合中
        contList = matchCont.findall(contentList.__getitem__(0))
        for cont in contList:
            print(cont)
            # 读出没段落（行）的内容
            engine.say(str(cont))
            engine.runAndWait()
        return nextpageURL

# ✨✨✨✨✨✨✨✨✨✨✨懒人听书程序开始✨✨✨✨✨✨✨✨✨✨✨✨
# 你想收听的书
searchBookName = '雪中悍刀行' #或者 '剑来'
# 懒人听书启动
readBook = readBook()
# 查找书本信息数据
url = "http://search.zongheng.com/s?keyword="
# 转码汉字转换成unicode
url_name =urllib.parse.quote(searchBookName)
# 把转码后的书名整合进去URL里面
url = url + url_name
try:
    # 首页输入书名 查找书名
    html = readBook.getHtml(url)
    # 返回查找到的书本URL
    bookURL = readBook.getSerachBookURL(html)
    # 根据上面URL取得 点击书籍详情
    html2 = readBook.getHtml(bookURL)
    # 得到开始阅读URL
    bookURL2 = readBook.getSerachBookURL2(html2, searchBookName)
    # 点击开始阅读 取得页面所有信息
    html3 = readBook.getHtml(bookURL2)
    # 取得第一章节的内容
    nextPage = readBook.getContext(html3, searchBookName)
    # 循环收听 前50 章节的内容
    pagNum = 1
    while pagNum < 50:
        pagNum = pagNum+1
        # 取得下一章节URL
        nextHtml = readBook.getHtml(nextPage.__getitem__(0))
        # 取得下一章节的内容
        nextPage = readBook.getContext(nextHtml, searchBookName)
except Exception as e :
    print(e)