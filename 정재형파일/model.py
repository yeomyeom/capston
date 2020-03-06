from sklearn import svm
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import chi2, SelectKBest
from joblib import dump


with open("adv.txt",'r',encoding='utf-8') as adv:
	advList = adv.readlines()
with open("nadv.txt", 'r', encoding='utf-8') as nadv:
	nadvList = nadv.readlines()

advnum = len(advList)
nadvnum = len(nadvList)

X = []
y = []

for i in range(advnum):
	y.append(1)

for i in range(nadvnum):
	y.append(0)

X.extend(advList)
X.extend(nadvList)

cv = CountVectorizer()
tft = TfidfTransformer()
sb = SelectKBest(chi2)

X = cv.fit_transform(X)
dump(cv, 'countvec.joblib')
X = sb.fit_transform(X, y)
dump(sb, 'select.joblib')
X = tft.fit_transform(X)
dump(tft, 'tf_trans.joblib')

svml = svm.SVC(kernel='linear', gamma='auto', probability=True)
svml.fit(X, y)
dump(svml, 'model.joblib')