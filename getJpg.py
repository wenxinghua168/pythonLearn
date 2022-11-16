import re
import urllib.request
import ssl
#定义爬虫类
class crawl:
    def getJpg(self):
        # url = "https://tieba.baidu.com/p/5008853571?fr=good"
        url = "https://www.toutiao.com/i6974222639716008459/"
        ssl._create_default_https_context = ssl._create_unverified_context
        page = urllib.request.urlopen(url)
        #抓取html的内容
        html = page.read().decode('UTF-8')
        print(html)
        #匹配规则 匹配 以src+" 开头的，中间有一个或者任意个字符， 后面接续.jpg" 最后结尾是size 的字符串
        reg =r'src="(.+?\.jpg)" size'
        imgReg = re.compile(reg)
        # 按上面的规则在HTML 内容找到图片
        imgList = imgReg.findall(html)
        path = '/Users/wenxinghua/Desktop/Project/local/'
        x = 0
        for img in imgList:
            #下载图片到本地，并且修改图片名字从0开始排序
            urllib.request.urlretrieve(img,'{0}{1}.jpg'.format(path,x))
            x = x + 1
            print(img)
#实体化类
callCrawl = crawl()
callCrawl.getJpg()