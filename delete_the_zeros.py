import os
import numpy as np

father=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))

#feature_train=np.load(father+'/JDATA用户购买时间预测_A榜/sub_sec_feature_train.npy')
#need_delete=[]
#for i in range(len(feature_train)):
#    if sum(feature_train[i])==0:
#        need_delete.append(i)
#feature_train=np.delete(feature_train,need_delete,0)

#feature_test=np.load(father+'/JDATA用户购买时间预测_A榜/sub_sec_feature_test.npy')
#need_delete=[]

#for i in range(len(feature_test)):
#    if sum(feature_test[i])==0:
#        need_delete.append(i)
#feature_test=np.delete(feature_test,need_delete,0)

#deletelist=[]
#for i in range(len(feature_test)):
#    if np.where((feature_test[i] ==feature_train).all(1))[0]!=[]:
#        deletelist.append(i)
#        print(i)
#print(deletelist)
#feature_train=np.delete(feature_train,deletelist,0)

#np.save(father+'/JDATA用户购买时间预测_A榜/sub_sec_feature_test_.npy',feature_test)
#np.save(father+'/JDATA用户购买时间预测_A榜/sub_sec_feature_train_.npy',feature_train)

# feature_predict=np.load(father+'/JDATA用户购买时间预测_A榜/feature_predict.npy')
# need_delete=[]
# for i in range(len(feature_predict)):
#     if sum(feature_predict[i])==0:
#         need_delete.append(i)
# feature_predict=np.delete(feature_predict,need_delete,0)
# np.save(father+'/JDATA用户购买时间预测_A榜/feature_predict.npy',feature_predict)
#
#
#
feature_all=np.load(father+'/JDATA用户购买时间预测_A榜/sub_sec_feature.npy')
need_delete=[]
for i in range(len(feature_all)):
    if sum(feature_all[i])==0:
        need_delete.append(i)
feature_all=np.delete(feature_all,need_delete,0)
np.save(father+'/JDATA用户购买时间预测_A榜/sub_sec_feature.npy',feature_all)

# print(feature_train)
# print(feature_test)
print(feature_all)
