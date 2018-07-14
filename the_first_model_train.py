import handle_feature
import xgboost as xgb
import numpy as np
import sys
import os
import math
father=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
X_pre,id_=handle_feature.read_predict()

def multi():
    [[X_train, Y_train], [X_test, Y_test]] = handle_feature.Muti_classification(700000)
    Y_train = Y_train - 1
    Y_test = Y_test - 1
    print(len(X_train))
    print(X_train)
    print(len(Y_train))
    print(Y_train)
    print(len(X_test))
    print(X_test)
    print(len(Y_test))
    print(Y_test)

    dtrain = xgb.DMatrix(X_train, label=Y_train)
    dtest = xgb.DMatrix(X_test, label=Y_test)
    watchlist = [(dtrain, 'train'), (dtest, 'test')]
    # 多分类模型
    param_multi = {"objective": "multi:softmax",
                 "eta": 0.15,
                 "max_depth": 6,
                 "subsample": 0.7,
                 "colsample_bytree": 0.7,
                 "silent": 1,
                 "learning_rate": 0.1,
                 'num_class': 31
                 }
    num_round = 100
    bst = xgb.train(param_multi, dtrain, num_round, early_stopping_rounds=10, evals=watchlist, verbose_eval=True)
    ypred = bst.predict(dtest)
    print(ypred)
    ylabel = ypred
    sum = 0
    ca = 0
    for i in range(len(Y_test)):
        ca += abs(int(ylabel[i] + 0.5) + 1 - Y_test[i])
        if int(ylabel[i] + 0.5) + 1 == Y_test[i]:
            sum += 1
    print(sum / len(Y_test))
    print(ca / len(Y_test))
    bst.save_model('../JDATA用户购买时间预测_A榜/xgboost_multi.model')

def reg():
    [[X_train, Y_train], [X_test, Y_test]]=handle_feature.Muti_classification()
    Y_test=Y_test
    print(len(X_train))
    print(X_train)
    print(len(Y_train))
    print(Y_train)
    print(len(X_test))
    print(X_test)
    print(len(Y_test))
    print(Y_test)
    f_name=['上一次购买目标品类时间','age','sex','user_lv_cd','purchase_gap','cate_purchase_gap','purchase/overview','purchase/watch','average_price']
    f_len=len(f_name)
    for i in range(f_len,len(X_train[0])):
        f_name.append(str(i))

    dtrain=xgb.DMatrix(X_train, label=Y_train)
    dtest=xgb.DMatrix(X_test, label=Y_test)
    watchlist = [(dtrain,'train'),(dtest,'test')]
    #回归模型
    param_reg = {"objective": "reg:linear",
                  "eta": 0.15,
                  "max_depth": 20,
                  "subsample": 0.7,
                  "colsample_bytree": 0.7,
                  "silent": 0,
                 "learning_rate":0.05,

                  }
    num_round=2000
    bst=xgb.train(param_reg, dtrain, num_round, early_stopping_rounds=10, evals=watchlist, verbose_eval=True)
    print(sorted(bst.get_fscore().items(),key=lambda x:-x[1]))
    ypred=bst.predict(dtest)
    print(ypred)
    ylabel = ypred
    sum=0
    ca=0
    for i in range(len(Y_test)):
        ca+=abs(int(ylabel[i]+0.5) - Y_test[i])
        if int(ylabel[i]+0.5) == Y_test[i]:
            sum+=1
    print(sum / len(Y_test))
    print(ca / len(Y_test))
    bst.save_model('../JDATA用户购买时间预测_A榜/xgboost_reg.model')

def binary():
#二分类
    [[X_train,Y_train],[X_test,Y_test]]=handle_feature.Two_classification()
    print(len(X_train))
    print(X_train)
    print(len(Y_train))
    print(Y_train)
    print(len(X_test))
    print(X_test)
    print(len(Y_test))
    print(Y_test)
    print(np.sum(Y_test))
    print('训练集的正负比为',np.sum(Y_train)/(len(Y_train)-np.sum(Y_train)))
    print('测试集的正负比为', np.sum(Y_test) / (len(Y_test) - np.sum(Y_test)))
    dtrain=xgb.DMatrix(X_train, label=Y_train)
    dtest=xgb.DMatrix(X_test, label=Y_test)
    watchlist = [(dtrain,'train'),(dtest,'test')]
    param_binary = {'max_depth':20,
                  'eta':0.1,
                  'silent':1,
                  'objective':'binary:logistic',
                    "learning_rate":0.1
                  }
    bst=xgb.train(param_binary,dtrain,num_boost_round=2000,early_stopping_rounds=10,evals=watchlist)
    ypred=bst.predict(dtest)
    print(ypred)
    ylabel=ypred
    sum=0
    for i in range(len(Y_test)):
        if int(ylabel[i]+0.5) == Y_test[i]:
            sum+=1
    print(sum / len(Y_test))
    bst.save_model('../JDATA用户购买时间预测_A榜/xgboost_binary.model')

if __name__=="__main__":
    if sys.argv[1]=='reg':
        reg()
    elif sys.argv[1]=='muti':
        multi()
    elif sys.argv[1]=='two':
        binary()
