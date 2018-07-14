from sklearn.model_selection import cross_val_score
import handle_feature
from sklearn.ensemble import AdaBoostClassifier
import os
import xgboost as xgb
from sklearn.externals import joblib
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
bst_binary = xgb.Booster(model_file='../JDATA用户购买时间预测_A榜/xgboost_binary.model')
bst_multi=xgb.Booster(model_file='../JDATA用户购买时间预测_A榜/xgboost_multi.model')
dpre=xgb.DMatrix(X_pre)
print(X_pre)
pred_binary=bst_binary.predict(dpre)
pred_multi=bst_multi.predict(dpre)

n=0
outcome_purchse=open(father+'/JDATA用户购买时间预测_A榜/outcome_purchase','w',encoding='utf-8')

for i in pred_binary:
    i_muti=int(pred_multi[n]+0.5)+1
    print(max(pred_multi))
    i_muti=max(i_muti,1)
    i_muti=min(i_muti,31)
    outcome_purchse.write(str(int(id_[n]))+','+date[i_muti+34+int(X_pre[n][2]*365+0.5)]+','+str(pred_binary[n])+'\n')
    n+=1
print(n)
