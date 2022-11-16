import time
import datetime
import pymysql
from bs4 import BeautifulSoup
import re
import urllib.request
import ssl
#定义爬虫类
class crawl:
    def getContent(self):
        url = "http://data.sports.sohu.com/nba/nba_schedule_by_day.php" #?teamid=0&d=2022-06-14&season_year=2009#new_page_begin
        ssl._create_default_https_context = ssl._create_unverified_context
        page = urllib.request.urlopen(url)
        # 抓取html的内容
        html = page.read().decode('GBK')
        soup = BeautifulSoup(html, 'html.parser')
        tab = soup.find(name="div", attrs={"class": "tab"})
        trList = tab.table.find_all('tr')
        index = 0
        for tr in trList:
            if index == 0:
                index = index + 1
                continue
            tr_tdList = tr.find_all('td')
            getLink = 0
            setTitleNBA = ""
            setTeamA = tr_tdList[2].get_text().replace(' ', '').replace('	', '').replace("\n", "").replace("\r","")
            setTeamB = tr_tdList[4].get_text().replace(' ', '').replace('	', '').replace("\n", "").replace("\r","")
            scoreAB = tr_tdList[3].get_text().replace(' ', '').replace('	', '').replace("\n", "").replace("\r","")
            scoreList = str(scoreAB).split("-")
            score = scoreList[0]
            score1 = scoreList[1]
            if int(score) < int(score1):
                setTitleNBA = setTitleNBA + setTeamB +score1 +" vs " +setTeamA  +score +" 取得比赛的胜利"
            else:
                setTitleNBA = setTitleNBA + setTeamA + score + " vs " + setTeamB + score1 + " 取得比赛的胜利"
            setTextCont = setTeamA + "\n" + "\r"
            setTextCont1 = setTeamB + "\n" + "\r"
            for td in tr_tdList:
                titleNBA = str(td.get_text()).replace(' ', '').replace('	', '').replace("\n", "").replace("\r", "")
                # setTitleNBA = setTitleNBA + titleNBA
                if getLink == 3:
                    linkInfo = td.find('a').get("href")
                    linkURL = "http://data.sports.sohu.com/nba/" + linkInfo
                    pageInfo = urllib.request.urlopen(linkURL)
                    htmlInfo = pageInfo.read().decode('GBK')
                    soup = BeautifulSoup(htmlInfo, 'html.parser')

                    # 取得第一节 到 第四节的内容信息
                    score_board = soup.find(id='score_board')
                    #找到table的行内容
                    score_tableList = score_board.table.find_all('table')
                    score_tdList = score_tableList[1].find_all('td')
                    # getCoreCont(score_tdList)
                    print(self.getCoreCont(score_tdList,setTeamA,setTeamB))
                    # 抓取第一队比赛的详细的内容
                    tav_team_stats = soup.find(id='v_team_stats')
                    # 找到table的行内容
                    trListInfo = tav_team_stats.table.find_all('tr')
                    indexInfo = 0
                    for trInfo in trListInfo:
                        # 跳过标题
                        if indexInfo == 0:
                            indexInfo = indexInfo + 1
                            continue
                        # 跳过7位 以后的球员信息
                        if indexInfo == 7:
                            break
                        tdList = trInfo.find_all('td')
                        setTextCont = setTextCont + self.getContentStr(tdList) # 取得每个球员的详细数据
                        indexInfo = indexInfo + 1

                    # 取得第一队的总计数据
                    totalTeamAtd = trListInfo[-2].find_all('td')
                    totalInfoA = self.getTotalTeamInfo(totalTeamAtd)
                    print(totalInfoA)

                    # 抓取第二队比赛的详细的内容
                    h_team_stats = soup.find(id='h_team_stats')
                    # 找到table的行内容
                    trListInfo1 = h_team_stats.find_all('tr')
                    indexInfo1 = 0
                    for trInfo in trListInfo1:
                        # 跳过标题
                        if indexInfo1 == 0:
                            indexInfo1 = indexInfo1 + 1
                            continue
                        # 跳过7位 以后的球员信息
                        if indexInfo1 == 7:
                            break
                        tdList = trInfo.find_all('td')
                        setTextCont1 = setTextCont1 + self.getContentStr(tdList)
                        indexInfo1 = indexInfo1 + 1
                    # 取得第二队的总计数据
                    totalTeamBtd = trListInfo1[-2].find_all('td')
                    totalInfoB = self.getTotalTeamInfo(totalTeamBtd)
                    print(totalInfoB)

                # 跳过没用的列
                if getLink == 4:
                    break
                getLink = getLink + 1
            index = index + 1
            date = datetime.datetime.now()
            date = str(date.year) + '年' + str(date.month) + '月' + str(date.day) + '日'
            print("北京时间",date, setTitleNBA)
            if int(score) < int(score1):
                print(setTextCont1)
                print(setTextCont)
            else:
                print(setTextCont)
                print(setTextCont1)
            print('✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨' + "\n" + "\r" +'(感谢你的支持：点赞➕关注 )')
            print('✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨')
            print("✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨分割线✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨")

    def getTdStr (self, str1):
        strRet = str1.replace(' ', '').replace('	', '').replace("\n", "").replace("\r", "")
        return strRet
    def getContentStr (self, tdList):
        player1 = self.getTdStr(tdList[1].get_text())# 球员名字1
        player2 = self.getTdStr(tdList[2].get_text())# 出场时间
        player3 = self.getTdStr(tdList[3].get_text())# 投篮
        player4 = self.getTdStr(tdList[4].get_text())# 其中三分球
        player5 = self.getTdStr(tdList[5].get_text())# 篮板
        player6 = self.getTdStr(tdList[6].get_text())# 失误
        player7 = self.getTdStr(tdList[7].get_text())# 篮板
        player8 = self.getTdStr(tdList[8].get_text())# 助攻
        player9 = self.getTdStr(tdList[9].get_text())# 命中
        player13 = self.getTdStr(tdList[13].get_text())# 得分
        # 得分的描述
        info = self.selectInfo('得分',player13)
        if int(player13) >= 15 :
            contentText = player1 + " 出场时间" + player2 + "分钟 "+" 全场砍下" + player13 + "分 "
        else:
            contentText = player1 + " 全场只得到" + player13 + "分 "
        if int(player7) >= 5:
            contentText = contentText + player7 +"篮板 "
        if int(player8) >= 5:
            contentText = contentText + player8 + "助攻 "

        if player4 != '0-0':
            list3point = str(player4).replace(' ', '').split('-')
            mingzhong = int(int(list3point[0])/int (list3point[1] ) * 100)
            if int(list3point[1]) > 6 :
                contentText = contentText +"其中三分球" + player4 + " "
                mingZhong = self.selectInfo('三分球命中率', str(mingzhong))#三分命中率描述
                contentText = contentText + mingZhong
            if int(list3point[0]) >= 8 :
                sanFen = self.selectInfo('三分', list3point[0])#三分命中率描述
                contentText = contentText + sanFen

        if int(player13) >= 15:
            contentText = contentText + "\n" + "\r" + info #得分
        if int(player7) >= 10:
            lanBanInfo = self.selectInfo('篮板', player7)#篮板
            contentText = contentText + "\n" + "\r" + lanBanInfo
        if int(player8) >= 10:
            zhuGongInfo = self.selectInfo('助攻', player8)#助攻
            contentText = contentText + "\n" + "\r" + zhuGongInfo
        return contentText + "\n" + "\r"
    def insertNBAMaster (self, key, value, info1, info2, info3):
        try:
            conn = pymysql.connect(host="localhost", user="root", passwd="root", db="database01", charset='utf8')
            insertContentSql = "INSERT INTO web_NBAMaster (nbaKey,nbaValue,info1,info2,info3)" + "VALUES(%s,%s,%s,%s,%s)"
            with conn.cursor() as cursor:
                cursor.execute(insertContentSql, [key, value, info1, info2, info3])
            conn.commit()
            conn.close()
        except Exception as e:
            print("列：insertNBAMaster---->error", e)

    def selectInfo (self, key, value):
        try:
            conn = pymysql.connect(host="localhost", user="root", passwd="root", db="database01", charset='utf8')
            with conn.cursor() as cursor:
                cursor.execute("select info1,info2,info3 from web_NBAMaster where nbaKey =%s and nbaValue =%s", [key, value])
            NBAInfo = cursor.fetchone()
            if NBAInfo:
                return str(NBAInfo[0]) + str(NBAInfo[1]) +str(NBAInfo[2])
            conn.close()
        except Exception as e:
            print("列：insertNBAMaster---->error", e)
    # 各节比分描述~
    def getCoreCont (self, score_tdList,setTeamA,setTeamB):
        sco1A = score_tdList[0].get_text()  # A队第1节得分
        sco2A = score_tdList[1].get_text()  # A队第2节得分
        sco3A = score_tdList[2].get_text()  # A队第3节得分
        sco4A = score_tdList[3].get_text()  # A队第4节得分
        sco1B = score_tdList[4].get_text()  # B队第1节得分
        sco2B = score_tdList[5].get_text()  # B队第2节得分
        sco3B = score_tdList[6].get_text()  # B队第3节得分
        sco4B = score_tdList[7].get_text()  # B队第4节得分
        i1A = int (score_tdList[0].get_text())  # A队第1节得分
        i2A = int (score_tdList[1].get_text())  # A队第2节得分
        i3A = int (score_tdList[2].get_text())  # A队第3节得分
        i4A = int (score_tdList[3].get_text())  # A队第4节得分
        i1B = int (score_tdList[4].get_text())  # B队第1节得分
        i2B = int (score_tdList[5].get_text())  # B队第2节得分
        i3B = int (score_tdList[6].get_text())  # B队第3节得分
        i4B = int (score_tdList[7].get_text())  # B队第4节得分
        if i1A >= i1B:
            scoContet1 = "第一节比赛：" + setTeamA + sco1A + " vs " + setTeamB + sco1B + " 暂时领先" + str(i1A -i1B) + "分"+ "\n" + "\r"
        else:
            scoContet1 = "第一节比赛：" + setTeamB + sco1B + " vs " + setTeamA + sco1A + " 暂时领先" + str(i1B - i1A) + "分"+ "\n" + "\r"
        # 2节
        if i2A >= i2B:
            scoContet2 = "第二节比赛：" + setTeamA + sco2A + " vs " + setTeamB + sco2B + " 领先" + str(i2A - i2B) + "分"+ "\n" + "\r"
        else:
            scoContet2 = "第二节比赛：" + setTeamB + sco2B + " vs " + setTeamA + sco2A + " 暂时领先" + str(i2B - i2A) + "分" + "\n" + "\r"
        if i1A + i2A > i1B + i2B:
            scoContet2 = scoContet2 + "半场结束：" + setTeamA + str(i1A + i2A) + " 领先" + setTeamB + \
                         str(i1A + i2A - i1B - i2B) + "分" + "\n" + "\r"
        elif i1A + i2A < i1B + i2B:
            scoContet2 = scoContet2 + "半场结束" + setTeamB + str(i1B + i2B) + " 领先" + setTeamA + \
                         str(i1B + i2B - i1A - i2A) + "分" + "\n" + "\r"
        else:
            scoContet2 = scoContet2 + "半场结束" + setTeamB + str(i1B + i2B) + "分" + " vs " + setTeamA + \
                         str(i1A + i2A) + "分。" + "双方战平，重新回到同一起跑线。" + "\n" + "\r"
        # 3节
        if i3A >= i3B:
            scoContet3 = "第三节比赛：" + setTeamA + sco3A + " vs " + setTeamB + sco3B + " 领先" + str(i3A - i3B) + "分" + "\n" + "\r"
        else:
            scoContet3 = "第三节比赛：" + setTeamB + sco3B + " vs " + setTeamA + sco3A + " 暂时领先" + str(i3B - i3A) + "分" + "\n" + "\r"
        if i1A + i2A + i3A > i1B+i2B+i3B:
            scoContet3 = scoContet3 + "三节战罢：" + setTeamA + str(i1A + i2A+ i3A) + " 领先" + setTeamB + \
                         str(i1A + i2A + i3A - i1B - i2B- i3B) + "分" + "\n" + "\r"
        elif i1A + i2A + i3A < i1B+i2B+i3B:
            scoContet3 = scoContet3 + "三节战罢：" + setTeamB + str(i1B + i2B+ i3B) + " 领先" + setTeamA +\
                         str(i1B + i2B + i3B- i1A - i2A - i3A) + "分" + "\n" + "\r"
        else:
            scoContet3 = scoContet3 + "三节战罢：" + setTeamB + str(i1B + i2B+ i3B) + "分"+  " vs " + setTeamA + \
                         str(i1A + i2A+ i3A) + "分。" + "双方三节战平，重新回到同一起跑线。"+ "\n" + "\r"
        # 4
        if i4A >= i4B:
            scoContet4 = "第四节比赛：" + setTeamA + sco4A + " vs " + setTeamB + sco4B + " 领先" + str(i4A - i4B) + "分"+ "\n" + "\r"

        else:
            scoContet4 = "第四节比赛：" + setTeamB + sco4B + " vs " + setTeamA + sco4A + " 暂时领先" + str(i4B - i4A) + "分"+ "\n" + "\r"

        return scoContet1 + scoContet2 + scoContet3 + scoContet4

    def getTotalTeamInfo (self, tdList):
        player3 = self.getTdStr(tdList[2].get_text())#投篮
        player4 = self.getTdStr(tdList[3].get_text())#三分
        player5 = self.getTdStr(tdList[4].get_text())#罚球
        player7 = self.getTdStr(tdList[6].get_text())#篮板
        player8 = self.getTdStr(tdList[7].get_text())#助攻
        player9 = self.getTdStr(tdList[8].get_text())#失误
        player12 = self.getTdStr(tdList[11].get_text())#犯规

        list3point = str(player4).replace(' ', '').split('-')
        mingzhong = int(int(list3point[0])/int (list3point[1] ) * 100)
        totalText = "其中三分球" + player4 + " "
        # mingZhong = self.selectInfo('三分球命中率', str(mingzhong))#三分命中率描述
        # totalText = totalText + mingZhong
        # sanFen = self.selectInfo('三分', list3point[0])#三分命中率描述
        # totalText = totalText + sanFen
        totalText = totalText + "、罚球：" + player5 + "、篮板：" + player7 + "、助攻：" + player8 + "、失误" + player9 + \
                      "、犯规：" + player12
        return totalText + "\n" + "\r"
#实体化类
callCrawl = crawl()
callCrawl.getContent()

lop = 0
while lop <= 1:
    # callCrawl.insertNBAMaster("出场时间",str(lop),"今天他告诉了全世界他的有多强,遇神杀神，佛挡杀佛","","")
    # callCrawl.insertNBAMaster("得分",str(lop),"极其惨淡的得分慌，进攻效率极其低下，完全失去了以往的手感","没有得分还能在场上待着，教练在赛场上的作用是什么？","整场酱油打得飞起，应该在板凳席上待着")
    # callCrawl.insertNBAMaster("得分命中率",str(lop),"今天他告诉了全世界他的得分爆发力有多强,遇神杀神，佛挡杀佛","比赛已经展现了无敌的状态，天人合一境界。一球在手，天下我有的霸气","他的身上有一种最为纯粹的古典英雄主义气息。那种救世主一样的表演,想必是每个少年心中幻想成为的角色")
    # callCrawl.insertNBAMaster("三分",str(lop),"今天单场命中"+ str(lop) + "记三分,今夜他为自己代言：五花马，三分球，与尔同消万古愁！","正如有句老话说的好：到老始知非力取，三分人事七分天。","")
    # callCrawl.insertNBAMaster("三分球命中率",str(lop),"本场的三分命中率是低于正常水平 只有" + str(lop) + "% " +"发挥失常，在三分线外没有对对方造成有效的杀伤。也没有让对手感觉到威胁。","","")
    # callCrawl.insertNBAMaster("篮板",str(lop),"因为出色的篮板球意识，加上身体上的天赋，让他在争夺中，屡屡占得先机，单场拿下" + str(lop) + "个篮板，一举化身成为了篮板王，在NBA的历史长河中留下了浓墨重彩的一页。","","")
    # callCrawl.insertNBAMaster("助攻",str(lop),"篮球只要一到他的手上，仿佛就有了魔力长了眼睛一般，不看人也可以把球舒适的送到队友手上，手起刀落，轻松得分。","他就是所谓控场大师，巧妙的穿针引线，激活带动全队的进攻。","")
    # callCrawl.insertNBAMaster("失误",str(lop),"全场都在梦游，亮瞎了大众的眼睛"," 全场各种失误，完全不堪入目。","")
    # callCrawl.insertNBAMaster("抢断",str(lop),"正常表现 没有获得机会去抢断","没有抢断，侵略性不够","没有抢断，侵略性不够，对手太强大了")
    lop = lop +1







