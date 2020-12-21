import re

phone = '15285468546'
ret = re.match('1[3-9]\d{9}', phone)
print(ret.group())