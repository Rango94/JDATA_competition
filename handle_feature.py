import os
import numpy as np
import random
from sklearn import preprocessing
father=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
feature_train=np.load(father+'/JDATA用户购买时间预测_A榜/sub_third_feature_train.npy')
feature_test=np.load(father+'/JDATA用户购买时间预测_A榜/sub_third_feature_test.npy')
feature_predict=np.load(father+'/JDATA用户购买时间预测_A榜/feature_predict_4.npy')
feature_all=np.load(father+'/JDATA用户购买时间预测_A榜/sub_third_feature.npy')
print(feature_all.shape)
print(feature_train.shape)
print(feature_test.shape)
print(feature_predict.shape)

print('正在归一化数据')
scalar=preprocessing.StandardScaler().fit(feature_all[:,2:])
feature_train[:,2:]=scalar.transform(feature_train[:,2:])
feature_test[:,2:]=scalar.transform(feature_test[:,2:])
feature_predict[:,1:]=scalar.transform(feature_predict[:,1:])
print('归一化数据完成')

def Two_classification(total=-1,positive=-1,negative=-1):
    return two_classification(feature_train,total,positive,negative),two_classification(feature_test,total,positive,negative)

def Muti_classification(total=-1,without_negative=True):
    return muti_classification(feature_train,total,without_negative),muti_classification(feature_test,total,without_negative)

def read_predict():
    return feature_predict[:,1:],feature_predict[:,0]

def two_classification(feature=feature_all,total=-1,positive=-1,negative=-1):
    if total>len(feature) or total==-1:
        total=len(feature)
    X=np.zeros((total,len(feature[1])-2))
    Y=np.zeros(total)
    if positive==-1 and negative==-1:
        if total==len(feature):
            X=feature[:,2:]
            Y=feature[:,1]
            for i in range(len(Y)):
                if Y[i]>31 or Y[i]<1:
                    Y[i]=0
                else:
                    Y[i]=1
        else:
            for i in range(total):
                idx=random.randint(0,len(feature)-1)
                X[i]=feature[idx,2:]
                Y[i]=feature[idx,1]
                if Y[i]<0:
                    Y[i]=0
                else:
                    Y[i]=1
    else:
        positive=int(total*(positive/(positive+negative)))
        negative=total-positive
        for i in range(total):
            while True:
                idx=random.randint(0,len(feature)-1)
                if feature[idx,1]>31 and negative>0:
                    X[i]=feature[idx,2:]
                    Y[i]=0
                    negative-=1
                    break
                if feature[idx,1]<32 and positive>0:
                    X[i]=feature[idx,2:]
                    Y[i]=1
                    positive-=1
                    break
    return X,Y

def muti_classification(feature=feature_all,total=-1,without_negative=True):
    if total>len(feature) or total==-1:
        total=len(feature)
    X=np.zeros((total,len(feature[1])-2))
    Y=np.zeros(total)
    i=0
    while i<total:
        idx=random.randint(0,len(feature)-1)
        if not without_negative:
            X[i]=feature[idx,2:]
            Y[i]=feature[idx,1]
        else:
            if feature[idx,1]!=-1 and feature[idx,1]>0 and feature[idx,1]<32:
                X[i]=feature[idx,2:]
                Y[i]=feature[idx,1]
                i+=1
    return X,Y





