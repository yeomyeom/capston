from sklearn.ensemble import AdaBoostClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from joblib import load

def mlmodel(texts):
    model = load('mlmodel.joblib')
    count_vec = CountVectorizer()
    tf_trans = TfidfTransformer()
    count = count_vec.fit_transform(texts)
    tfval = tf_trans.fit_transform(count)
    return model.predict(tfval)