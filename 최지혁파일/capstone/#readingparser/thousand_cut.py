q = open("url.txt",'r')
file = open('url_baby_adv.txt','w')

filecontent = q.readlines()
lineNum = 0
list =[]
for i in filecontent:
    file.write(i)
    lineNum += 1
    if(lineNum == 999):
        print(i)
        break
print('check Num')
checkq = open("input1000_1.txt",'r')
checkqLine = checkq.readlines()
print(len(checkqLine))
