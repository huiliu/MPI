#!/export/home/liuhui/opt/bin/python3

import re
from urllib.request import urlopen
from multiprocessing import Process, Manager

#线路列表：
#'<li><span>.*?<\/li>', '(?<=>).*?<', '".*?"'
#当前页面线路列表：
#'<li><a href=.*?>.*?<\/li>', '<a .*?>.*?<\/a>', '".*?"'
#
#
#提取公交信息：发车时间等
#'(?<=<\/h2><li>).*?<\/a>', '<.*a.*?>', '查公交上八六八四cn'
#路线站点，第一个为去程，后为回程
#'(?<=：<span>).*?<\/span>', '[\u2E80-\u9FFF]+\({0,}[\u2E80-\u9FFF]+\){0,}[\u2E80-\u9FFF]*?'
#备注信息
#'(?<=备注信息<\/h2).*?<br'
#更新日期：
#'(?<=botm\(").*?"'


city = 'http://xiamen.8684.cn'

def readData(url, data=[], code='gbk'):
    tmp = urlopen(url).read().decode(code)
    data.append(tmp)
    return tmp

def getLineTypeList(html,reg=['<li><span>.*?<\/li>', '(?<=>).*?<', '(?<==).*?>']):
    """
        This Function use to get the archive of all line type.
        return a list contain all href.
    """
    allType = re.findall(reg[0], html)[0]
    return [ city + '/' + x[:-1] for x in re.findall( reg[2], allType )]

def getLineList(html, lineURL={}, reg = ['<li><a href=.*?>.*?<\/li>', '>.*?<', '".*?"']):
    """
        This function use to get the arch of the line in current page.
        return a list contain all href.
    """
    # Some whitespace character such as \n\t should effect regular match
    #so it is a better choice than eliminate it firstly.
    html = re.sub('\n|\t', '', html)
    d = re.findall('<div class=.la.><ul>.*?<\/ul>', html)[0]
    allline = re.findall(reg[0], d)
    for line in allline:
        name = re.findall(reg[1], line[4:-8] )[0][1:-1]
        href = city + re.findall(reg[2], line )[0][1:-1]
        lineURL[name] = href
    return lineURL

def getAllLineList( htmlDataList ):
    """
        This function use to read all line data that contain
        the name of line and it's href
    """
    i = 0
    num = len(htmlDataList)

    #use to share data between process, may be need modify in order to
    #promote efficient
    manager = Manager()
    LineList = manager.dict()

#   LineList = []
    while i < num:
        procline = Process(target=getLineList, args=(htmlDataList[i], LineList,))
        procline.start()
#       procline.join()
#       LineList.append(getLineList(htmlDataList[i]))
        i += 1
    return LineList

def getAllListPage():
    """
        Thist Function use to get the all line about the city
        which you want to get
    """
    firstPage = city + '/line1'
    data = urlopen(firstPage).read().decode('gbk')
    urlList = getLineTypeList(data)
    urlList.append(firstPage)
    num = len(urlList)
    i = 0
    manager = Manager()
    pageData = manager.list()
#   pageData = []
    while i < num:
        procline = Process(target=readData, args=(urlList[i], pageData,))
        procline.start()
#       procline.join()
#       pageData.append( readData(urlList[i]) )
        i += 1
    return pageData

def getLine(linehrefList):
    i = 0
def getLineInformation(html, reg=['(?<=<\/h2><li>).*?<\/a>', '<.*a.*?>', '查公交上八六八四cn']):
    """
        This function get information of the Line about start time, work time and so on.
    """
    tmp = re.findall(reg[0], html)[0]
    Info = re.sub(reg[1], '', tmp)
    info = re.sub(reg[2], '', Info)
    return info

def getStation(html, reg=['(?<=：<span>).*?<\/span>', '[\u2E80-\u9FFF]+\({0,}[\u2E80-\u9FFF]+\){0,}[\u2E80-\u9FFF]*?']):
    """
        This function use to get Station name
    """
    tmp = re.findall(reg[0], html)
    return [re.findall(reg[1], tmp[0]), re.findall(reg[1], tmp[1])]

def getNote(html, reg='(?<=备注信息<\/h2).*?<br'):
    """
    """
    return re.findall(reg, html)[0][2:-3]

def getUpdatTime(html, reg='(?<=botm\(").*?"'):
    return re.findall(reg, html)[0][:-1]

if __name__ == '__main__':
    d = getAllListPage()
    print(getAllLineList(d))
