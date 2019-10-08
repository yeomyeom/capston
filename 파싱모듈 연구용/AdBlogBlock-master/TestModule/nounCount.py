# -*- coding: utf-8 -*-
from konlpy.tag import Okt
from collections import Counter
import re, os
from pathlib import Path
# nouns로 분석 중 heap corruption으로 프로세스가 꺼지는 문제:
# emoji 때문으로 아래의 함수를 이용하여 emoji들을 없애면 해결됨.

def strip_e(st):
    RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
    return RE_EMOJI.sub(r'', st)

path = Path(__file__).parent

f = open(os.path.join(path,"DataA.txt"), "r",encoding='utf8')
lines = f.read()
lines = strip_e(lines)
nlpy = Okt()
nouns = nlpy.nouns(lines)
count = Counter(nouns)
tag_count = []
tags = []
for n, c in count.most_common(200):
    dics = {'tag': n, 'count': c}
    if len(dics['tag']) >= 2 and len(tags) <= 99:
        tag_count.append(dics)
        tags.append(dics['tag'])

f = open(os.path.join(path,"statistic.txt"), "w" ,encoding='utf8')

for tag in tag_count:
    f.write("{}위\t {:<14}\t".format(tag_count.index(tag)+1,tag['tag']))
    f.write("{}\n".format(tag['count']))
print("success!")
f.close()