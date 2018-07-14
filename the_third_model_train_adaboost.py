import handle_feature
from sklearn.model_selection import cross_val_score
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.externals import joblib
import numpy as np
import sys
import os
import math
father=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
X_pre,id_=handle_feature.read_predict()

def multi():
    [[X_train_, Y_train_], [X_test_, Y_test_]] = handle_feature.Muti_classification(700000)
    X_train=[]
    Y_train=[]
    X_test=[]
    Y_test=[]
    for i in range(len(Y_train_)):
        if Y_train_[i]>0 and Y_train_[i]<32:
            X_train.append(X_train_[i])
            Y_train.append(Y_train_[i])

    for i in range(len(Y_test_)):
        if Y_test_[i]>0 and Y_test_[i]<32:
            X_train.append(X_test_[i])
            Y_train.append(Y_test_[i])
    X_train=np.array(X_train)
    Y_train=np.array(Y_train)
    X_test=np.array(X_test)
    Y_test=np.array(Y_test)

    print(X_train)
    print(Y_train)
    print(X_test)
    print(Y_test)

    print('开始训练')
    clf = AdaBoostClassifier(DecisionTreeClassifier(max_depth=10, min_samples_split=5, min_samples_leaf=5), n_estimators=200, learning_rate=0.05, algorithm='SAMME.R')
    clf.fit(X_train,Y_train)
    joblib.dump('../JDATA用户购买时间预测_A榜/adaboost_multi.model')

if __name__=="__main__":
    if sys.argv[1]=='muti':
        multi()

