#!/export/home/liuhui/opt/bin/python3

from urllib.request import urlopen
import re

data = urlopen('http://xiamen.8684.cn/line1').read().decode('gbk')
print(data)
reg = re.compile('<li><span>.*?<\/span>.*?<\/li>')
print(reg.findall(data))
