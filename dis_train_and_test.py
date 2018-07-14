import os
import numpy as np
father=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))

feature=np.load(father+'/JDATA用户购买时间预测_A榜/sub_third_feature.npy')

print(feature)
Tr=int(len(feature)/10)*8+min(len(feature)%10,8)
Te=len(feature)-Tr

train=np.zeros((Tr,len(feature[1])))
test=np.zeros((Te,len(feature[1])))

tr=0
te=0
for i in range(len(feature)):
    if i%10<8:
        train[tr]=feature[i]
        tr+=1
    else:
        test[te]=feature[i]
        te+=1
np.save(father+'/JDATA用户购买时间预测_A榜/sub_third_feature_train.npy',train)
np.save(father+'/JDATA用户购买时间预测_A榜/sub_third_feature_test.npy',test)






