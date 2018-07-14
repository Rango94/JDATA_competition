#建立用户的商品的用户表示模型



import my_dic
import numpy as np
import os
father=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
user_action_seq=open(father+"/JDATA用户购买时间预测_A榜/user_action_seq.txt","r",encoding="utf-8")
user_dic=my_dic.user_info_dic
sku_dic=my_dic.sku_info_dic

#商品特征 {1#price 2-7#cate_ont-hot 8#para_1 9#para_2 10#para_3}
'''
para_1 均值187.834 max=475292.99 min=0.08
para_2 均值-0.0705944 max=6 min=-1 枚举类型没有0
para_3 均值-0.117117 max=7 min=-1 枚举类型没有0
'''
sku_feature_dic=np.zeros((len(sku_dic),10))
price_numpy=np.zeros(len(sku_dic))
para_1_numpy=np.zeros(len(sku_dic))
n=0
sku_dic_keys=sku_dic.keys()

for key in sku_dic_keys:
    price_numpy[n]=float(sku_dic[key]['price'])
    para_1_numpy[n]=float(sku_dic[key]['para_1'])
    n+=1

price_mean=np.mean(price_numpy)
price_std=np.std(price_numpy)

para_1_mean=np.mean(para_1_numpy)
para_1_std=np.std(para_1_numpy)

price_dic={}
para_1_dic={}

for i in range(len(price_numpy)):
    price_dic[price_numpy[i]]=(price_numpy[i]-price_mean)/price_std
    para_1_dic[para_1_numpy[i]]=(para_1_numpy[i]-para_1_mean)/para_1_std

sku_feature=np.zeros((len(sku_dic),11))
n=0
for key in sku_dic_keys:
    key_feature=np.zeros(11)
    key_feature[0]=int(key)
    key_feature[1]=price_dic[float(sku_dic[key]['price'])]
    if sku_dic[key]['cate']=='71':
        key_feature[2]=1
    if sku_dic[key]['cate']=='46':
        key_feature[3]=1
    if sku_dic[key]['cate']=='83':
        key_feature[4]=1
    if sku_dic[key]['cate']=='101':
        key_feature[5]=1
    if sku_dic[key]['cate']=='1':
        key_feature[6]=1
    if sku_dic[key]['cate']=='30':
        key_feature[7]=1
    key_feature[8]=para_1_dic[float(sku_dic[key]['para_1'])]
    key_feature[9]=(int(sku_dic[key]['para_2'])+1)/7
    key_feature[10]=(int(sku_dic[key]['para_2'])+1)/8
    sku_feature[n]=key_feature
    n+=1
np.save(father+"/JDATA用户购买时间预测_A榜/sku_feature.npy",sku_feature)
print(sku_feature[:10,:])
#用户特征 {1#age 2#sex 3#user_lv_cd 4#gap}
'''
用户的年龄是归一化后的枚举类型，从1到6，未知的是-1
用户等级从1到5
'''
# for i in user_dic['1']:
#     print(i+'\t',end='')
'''
age	sex	user_lv_cd	purchase_gap	cate_purchase_gap	
purchase/overview	purchase/watch	overview_1	overview_2	overview_3	
overview_4	overview_5	overview_6	overview_7	overview_8	
overview_9	overview_10	overview_11	overview_12	watch_1	
watch_2	watch_3	watch_4	watch_5	watch_6	
watch_7	watch_8	watch_9	watch_10	watch_11	
watch_12	purchase_1	purchase_2	purchase_3	purchase_4	
purchase_5	purchase_6	purchase_7	purchase_8	purchase_9	
purchase_10	purchase_11	purchase_12	average_price
'''
user_price=np.zeros(len(user_dic))

sku_num_s={
    'overview':{'71':np.zeros(len(user_dic)),'46':np.zeros(len(user_dic)),'83':np.zeros(len(user_dic)),'101':np.zeros(len(user_dic)),'1':np.zeros(len(user_dic)),'30':np.zeros(len(user_dic))},
    'watch':{'71':np.zeros(len(user_dic)),'46':np.zeros(len(user_dic)),'83':np.zeros(len(user_dic)),'101':np.zeros(len(user_dic)),'1':np.zeros(len(user_dic)),'30':np.zeros(len(user_dic))},
    'purchase':{'71':np.zeros(len(user_dic)),'46':np.zeros(len(user_dic)),'83':np.zeros(len(user_dic)),'101':np.zeros(len(user_dic)),'1':np.zeros(len(user_dic)),'30':np.zeros(len(user_dic))}
}
sku_num_s_mean={
    'overview':{'71':0,'46':0,'83':0,'101':0,'1':0,'30':0},
    'watch':{'71':0,'46':0,'83':0,'101':0,'1':0,'30':0},
    'purchase':{'71':0,'46':0,'83':0,'101':0,'1':0,'30':0}
}
sku_num_s_std={
    'overview':{'71':0,'46':0,'83':0,'101':0,'1':0,'30':0},
    'watch':{'71':0,'46':0,'83':0,'101':0,'1':0,'30':0},
    'purchase':{'71':0,'46':0,'83':0,'101':0,'1':0,'30':0}
}
n=0
for key in user_dic:
    user_price[n]=float(user_dic[key]['average_price'])
    for action in sku_num_s:
        for cate in sku_num_s[action]:
            sku_num_s[action][cate][n]=int(user_dic[key][action+'_num_'+cate])
    n+=1

for action in sku_num_s:
    for cate in sku_num_s[action]:
        sku_num_s_mean[action][cate]=np.mean(sku_num_s[action][cate])
        sku_num_s_std[action][cate]=np.std(sku_num_s[action][cate])
print(sku_num_s_mean)
print(sku_num_s_std)
average_price_average=np.mean(user_price)
average_price_std=np.std(user_price)


total_cate = ['71', '46', '83', '101', '1', '30']
n=0
user_feature=np.zeros((len(user_dic),len(user_dic['1'].keys())+1))
for key in user_dic:
    key_feature=np.zeros(len(user_dic['1'].keys())+1)
    key_feature[0]=int(key)
    key_feature[1]=(int(user_dic[key]['age'])+1)/7
    key_feature[2]=(int(user_dic[key]['sex']))/2
    key_feature[3]=(int(user_dic[key]['user_lv_cd'])-1)/4
    key_feature[4]=(int(user_dic[key]['purchase_gap']))/365
    key_feature[5] = (int(user_dic[key]['cate_purchase_gap'])) / 365
    key_feature[6] = float(user_dic[key]['purchase/overview'])
    key_feature[7] = float(user_dic[key]['purchase/watch'])
    key_feature[8] = (float(user_dic[key]['average_price']) - average_price_average) / average_price_std

    b=9
    for i in ['overview','watch','purchase']:
        for cate in total_cate:
            key_feature[b] = ((int(user_dic[key][i +'_num_'+ cate]))-sku_num_s_mean[i][cate])/sku_num_s_std[i][cate]
            b += 1
    for i in ['overview_gap_','watch_gap_','purchase_gap_']:
        for num in range(1,13):
            key_feature[b]=(int(user_dic[key][i+str(num)]))/365
            b+=1
    user_feature[n]=key_feature
    n+=1

np.save(father+"/JDATA用户购买时间预测_A榜/user_feature.npy",user_feature)
print(user_feature[:10,:])
