#第一次尝试提取用户序列特征
import os
import my_dic
import numpy as np
import random
father=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))

user_action_seq=open(father+"/JDATA用户购买时间预测_A榜/user_action_seq.txt","r",encoding="utf-8")
feature_head=open(father+"/JDATA用户购买时间预测_A榜/feature_head.txt","w",encoding="utf-8")

sku_info_dic=my_dic.sku_info_dic
user_info_dic=my_dic.user_info_dic

sku_feature=my_dic.sku_feature_dic
user_feature=my_dic.user_feature_dic

sku_len=len(sku_feature['1'])
user_len=len(user_feature['1'])

#为了更好的保存用户对商品的行为特征，我们不能对浏览和关注取one-hot，所以这里设浏览权重为1，关注权重为3,购买权重为10

action_weight={}
action_weight['1']=1
action_weight['2']=3
action_weight['100']=10

def build_feature(seq):
    outnumpy=np.zeros(sku_len*len(seq))
    for i in range(len(seq)):
        if seq[i]=="0":
            each_feature=np.zeros(sku_len)
        else:
            each_feature=np.zeros(sku_len)
            for each_sku in seq[i].split(','):
                each_sku=each_sku.split('-')
                try:
                    each_feature+=sku_feature[each_sku[0]]*action_weight[each_sku[1]]
                except:
                    print(each_sku)
        outnumpy[i*sku_len:(i+1)*sku_len]=each_feature
    return outnumpy


#我决定随机取窗口,再计算未来一个月内是否有购买记录

next(user_action_seq)
line=user_action_seq.readline()

feature=np.zeros((98924*100,306))
n=0
while line!="":
    line=line.replace("\n","").split("\t")
    for k in range(100):
        idx=random.randint(1,305)
        windows_feature=np.append(np.array([idx/365]),np.append(user_feature[line[0]],build_feature(line[idx:idx+30])))
        gap=-1
    #计算下一次购买时间
        for i in range(idx+30,idx+60):
            if '-100' in line[i]:
                if sku_info_dic[line[i].split('-')[0]]['cate']=='101' or sku_info_dic[line[i].split('-')[0]]['cate']=='30':
                    gap=i-idx-29
                    break
        windows_label=gap
        a_feature=np.append(windows_label,windows_feature)
        feature[n]=a_feature
        if random.random()>0.99:
            for a in a_feature:
                feature_head.write('%.4f'%a+"\t")
            feature_head.write('\n')
        n+=1
    line=user_action_seq.readline()

np.save(father+'/JDATA用户购买时间预测_A榜/first_feature.npy',feature)




