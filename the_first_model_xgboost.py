from sklearn.model_selection import cross_val_score
import handle_feature
from sklearn.ensemble import AdaBoostClassifier
import xgboost as xgb
import numpy as np
import os
import math
father=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
date={}
n=0
for each in open(father+'/JDATA用户购买时间预测_A榜/datefile.txt','r',encoding='utf-8').readline().replace('\n','').split(','):
    date[n]=each
    n+=1
for i in range(1,32):
    if i<10:
        date[n]='2017-05-0'+str(i)
    else:
        date[n]='2017-05-'+str(i)
    n+=1
X_pre,id_=handle_feature.read_predict()

[[X_train,Y_train],[X_test,Y_test]]=handle_feature.Muti_classification(200000)
X_muti,Y_muti=handle_feature.muti_classification(total=200000)
X_two,Y_two=handle_feature.two_classification()

print(X_train)
print(Y_train)
print(X_test)
print(Y_test)
dtrain=xgb.DMatrix(X_train,label=Y_train-1)
dtest=xgb.DMatrix(X_test,label=Y_test-1)
watchlist = [(dtrain,'train'),(dtest,'test')]
bst = xgb.XGBRegressor(max_depth=6, learning_rate=0.5, n_estimators=500, silent=0, objective='reg:gamma')
bst.fit(X_train,Y_train)
#param = {'max_depth':6, 'eta':0.5, 'eval_metric':'merror', 'silent':1, 'objective':'reg:gamma', 'num_class':30}
#bst=xgb.train(param,dtrain,num_boost_round=100,evals=watchlist)
#bst = xgb.Booster(model_file='../JDATA用户购买时间预测_A榜/xgboost.model')
ypred=bst.predict(Y_test)
print(ypred)
#for i in range(len(Y_test)):
#    print(str(Y_test[i])+'-'+str(int(ypred[i]+0.5)+1))
ylabel = ypred
sum=0
ca=0
for i in range(len(Y_test)):
    ca+=abs(int(ylabel[i]+0.5)+1-Y_test[i])
    if int(ylabel[i]+0.5)+1 == Y_test[i]:
        sum+=1
print(sum/len(Y_test))
print(ca/len(Y_test))
#print((sum( int(ylabel[i])+1 == Y_test[i] for i in range(len(Y_test))) / float(len(Y_test)) ))
#bst.get_booster().save_model('../JDATA用户购买时间预测_A榜/xgboost.model')
from sklearn import metrics

#print('AUC: %.4f' % metrics.roc_auc_score(Y_test,ypred))





#clf_two=AdaBoostClassifier(n_estimators=150,learning_rate=1)
#clf_two.fit(X_two,Y_two)

#clf_muti=AdaBoostClassifier(n_estimators=150,learning_rate=1)
#clf_muti.fit(X_muti,Y_muti)

#n=0
#outcome_purchse=open(father+'/JDATA用户购买时间预测_A榜/outcome_purchse','w',encoding='utf-8')
#outcome_unpurchse=open(father+'/JDATA用户购买时间预测_A榜/outcome_unpurchse','w',encoding='utf-8')

#for i in clf_two.predict(X_pre):
#    if i==1:
#        i_muti=clf_muti.predict([X_pre[n]])
#        outcome_purchse.write(str(int(id_[n]))+','+date[i_muti[0]+30+int(X_pre[n][0]*365+0.5)]+','+str(max(clf_muti.predict_proba([X_pre[n]])[0])*max(clf_two.predict_proba([X_pre[n]])[0])*100)+'\n')
#    else:
#        i_muti=clf_muti.predict([X_pre[n]])
#        outcome_unpurchse.write(str(int(id_[n]))+','+date[i_muti[0]+30+int(X_pre[n][0]*365+0.5)]+'\n')
#    n+=1
    #scores = cross_val_score(clf, X_train, Y_train)
    #print(scores.mean())
