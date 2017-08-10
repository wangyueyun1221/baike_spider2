# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import urllib2
import time
k=0
while k<10:
    url = "http://www.pm25.com/city/shanghai.html"
    html = urllib2.urlopen(url,timeout=10).read()
    if not html:
        print ("抓取网页失败")
        break
    doms = BeautifulSoup(html,"html.parser",from_encoding='utf-8')
    TagList=doms.select('.pj_area_data_details')
    if not len(TagList):
        print ("获取dom失败")
        break
    Lilist = TagList[0].select('li')
    finainfo=[]
    i=0
    while i < len(Lilist):
        info ={}
        info['location']=Lilist[i].find('a',class_='pjadt_location').get_text().encode('utf-8')
        # info['AQI']=Lilist[i].find('span',class_='pjadt_aqi').get_text()
        info['PM2.5']=Lilist[i].find('span',class_='pjadt_pm25').get_text().encode('utf-8')
        finainfo.append(info)
        i=i+1

    # print(finainfo)
    # for name,data in enumerate(finainfo):
    fout = open('outputresult.csv','w')
    fout.write ("<html>")
    fout.write ("<head><meta charset='utf-8'>")
    fout.write ("</head>")
    fout.write ("<body>")
    fout.write ("<table>")
    for index,data in enumerate(finainfo):
            fout.write ("<tr>")
            fout.write ("<td>%s</td>" % finainfo[index]['location'])
            fout.write ("<td>%s</td>" % finainfo[index]['PM2.5'])
            fout.write ("</tr>")



    fout.write ("</table>")
    fout.write ("</body>")
    fout.write ("</html>")
k=k+1
print('这是今天的第%d次统计'% (k+1))
time.sleep(3600)
fout.close()