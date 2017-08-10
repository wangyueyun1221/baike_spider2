# -*- coding: utf-8 -*-
import re
import urllib
import socket
from bs4 import BeautifulSoup

'''设置全局超时时间'''
socket.setdefaulttimeout(60)
''' 获取网页 '''
url = 'http://www.xs.la/8_8444'
print('抓取网页：%s' % url)
html = urllib.urlopen(url).read()
if not html:
    print('未抓取到网页')
    exit(0)

''' 获取dom '''
print('获取列表页dom')
dom = BeautifulSoup(html)
if not dom:
    print('未获取到dom')
    exit(0)

''' 获取小说列表dom '''
print('获取小说列表dom')
storyTagList = dom.select('div#list dd')
if not len(storyTagList):
    print('列表为空')
    exit(0)

''' 获取小说列表 '''
print('获取小说列表')
storyList = []
for tag in storyTagList:
    ''' 获取a标签 '''
    aTag = tag.select('a')
    if not len(aTag):
        continue
    ''' 判断style是否为空，若不为空，则跳过  '''
    if aTag[0].get('style'):
        continue
    storyInfo = {}
    storyInfo['name'] = aTag[0].string.encode("utf8")
    storyInfo['href'] = aTag[0]["href"]
    storyList.append(storyInfo)
if not len(storyList):
    print('格式化列表失败')
    exit(0)

'''遍历列表，获取章节内容'''
compeleteList = {}
articleFileHandler = open('./story.txt', 'w')
for index, chapterInfo in enumerate(storyList):
    chapterName = chapterInfo['name']
    if compeleteList.has_key(chapterName):
        continue
        pass
    else:
        compeleteList[chapterName] = chapterName;
        pass
    try:
        articleUrl = "%s%s" % ('http://www.xs.la', chapterInfo['href'])
        print('获取章节：%s' % chapterName)
        html = urllib.urlopen(articleUrl).read()
        if not html:
            raise Exception('未获取到%s的内容' % (chapterName))
        print('获取章节dom')
        dom = BeautifulSoup(html)
        if not dom:
            raise Exception('未获取到dom')
            pass
        '''获取章节内容dom'''
        print('获取章节内容dom')
        contentTags = dom.select('div#content')
        if not len(contentTags):
            raise Exception('内容为空')
            pass
        '''解析章节内容'''
        print('解析章节内容')
        contentTagsStr = str(contentTags[0])
        contentFormat = re.sub(r'<br.*?/?>|</?div.*>|<script.*t>|\&.*?;|　| ', "\n", contentTagsStr)
        contentList = contentFormat.split("\n")
        contentStr = ''
        '''拼接章节内容'''
        print('拼接章节内容')
        for paragraph in contentList:
            paragraph = str(paragraph)
            paragraph = paragraph.strip()
            if len(paragraph) == 0:
                continue
                pass
            # contentStr += '<p>';
            contentStr += str(paragraph);
            # contentStr += '</p>';
            contentStr = contentStr.replace('"', "'")
            contentStr = contentStr.replace("'", "'")
        '''写文件'''
        articleFileHandler.writelines(chapterName + "\n")
        articleFileHandler.writelines(contentStr + "\n")
    except Exception as e:
        print(e)
'''写完文件，关闭'''
articleFileHandler.close()
print('小说抓取完毕')