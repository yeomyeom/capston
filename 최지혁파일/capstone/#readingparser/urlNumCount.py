myFile = open('url.txt','r')
f = open("nonAdvInputIT.txt",'w')

filecontent = myFile.readlines()
new = []
i = 0
for url in filecontent:
    if('blog.naver.com' in url):
        i +=1
        f.write(url)
        print(url)
print(i)
myFile.close()
f.close()

'''url = open("input1000_1.txt",'r')
damn454 = url.readlines()
print(damn454[453])
'''