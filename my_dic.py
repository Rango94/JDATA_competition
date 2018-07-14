#用户和商品字典
import os
import numpy as np
_father=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
sku_info_dic=eval(open(_father+"/JDATA用户购买时间预测_A榜/sku_basic_info_dic.txt","r",encoding="utf-8").read())
user_info_dic=eval(open(_father+"/JDATA用户购买时间预测_A榜/user_basic_info_dic.txt","r",encoding="utf-8").read())

sku_feature_dic={}
try:
    sku_feature_numpy=np.load(_father+"/JDATA用户购买时间预测_A榜/sku_feature.npy")
    for i in sku_feature_numpy:
        sku_feature_dic[str(int(i[0]))]=i[1:]
except:
    print("sku_feature加载过程出现问题")
#print(sku_feature_dic)	
user_feature_dic={}
try:
    user_feature_numpy=np.load(_father+"/JDATA用户购买时间预测_A榜/user_feature.npy")
    for i in user_feature_numpy:
        user_feature_dic[str(int(i[0]))]=i[1:]
except:
    print("user_feature加载过程出现问题")
#print(user_feature_dic)
