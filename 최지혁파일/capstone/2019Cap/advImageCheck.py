import pickle
from collections import Counter

'''def adjust():
    return 1'''
def advImgChecker():


    data_dir = 'picture_adv.txt'
    fread = open(data_dir, 'r', encoding="ANSI")

    # \n 제거
    line = fread.readlines()
    newline = []
    for i in line:
        if '\n' in i:
            temp = i
            newline.append(temp.replace('\n', ''))
        else:
            newline.append(i)
    print(newline)

    # 한 url씩 나누기
    newnewline = []
    for i in newline:
        newnewline += (i.split())
    print(newnewline)

    #
    cnt = Counter(newnewline)
    print(cnt)


advImgChecker()


