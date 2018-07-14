import handle_feature
import os
import xgboost as xgb
import random
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
print(X_pre.shape)
print(id_)
bst_multi=xgb.Booster(model_file='../JDATA用户购买时间预测_A榜/xgboost_reg_local_test.model')
bst_binary=xgb.Booster(model_file='../JDATA用户购买时间预测_A榜/xgboost_binary_local_test.model')
dpre=xgb.DMatrix(X_pre)
print(X_pre)
pred_reg=bst_multi.predict(dpre)
pred_binary=bst_binary.predict(dpre)
n=0
outcome_purchse=open(father+'/JDATA用户购买时间预测_A榜/outcome_purchase','w',encoding='utf-8')

for i in pred_reg:
    gap=i
    if i>31.5 or i<0.5:
        print(i,'XXXXXXXXXXX')
        gap=random.randint(0,30)+0.5
    print(i)
    outcome_purchse.write(
        str(int(id_[n])) + ',' + date[334 + int(gap + 0.5)] + ',' + str('%.5f' % pred_binary[n]) + '\n')
    n+=1
print(n)
