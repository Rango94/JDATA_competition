#第二次尝试提取需要预测的用户序列特征
import os
import my_dic
import numpy as np
import random
father=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))

user_action_seq=open(father+"/JDATA用户购买时间预测_A榜/user_action_seq.txt","r",encoding="utf-8")

sku_info_dic=my_dic.sku_info_dic
user_info_dic=my_dic.user_info_dic

sku_feature=my_dic.sku_feature_dic
user_feature=my_dic.user_feature_dic

sku_len=len(sku_feature['1'])
user_len=len(user_feature['1'])

# 为了更好的保存用户对商品的行为特征，我们不能对浏览和关注取one-hot，所以这里设浏览权重为1，关注权重为3,购买权重为10


def have_purchase(subline):
    if '-' not in subline:
        return False
    for each in subline.split(','):
        if each.split('-')[1] == '3':
            if sku_info_dic[each.split('-')[0]]['cate'] == '101' or sku_info_dic[each.split('-')[0]]['cate'] == '30':
                return True
    return False

def have_purchase_spe(subline,cate):
    if '-' not in subline:
        return False
    for each in subline.split(','):
        if each.split('-')[1] == '3':
            if sku_info_dic[each.split('-')[0]]['cate'] == cate:
                return True
    return False

def have_overview_spe(subline,cate):
    if '-' not in subline:
        return False
    for each in subline.split(','):
        if each.split('-')[1] == '1':
            if sku_info_dic[each.split('-')[0]]['cate'] == cate:
                return True
    return False

def have_watch_spe(subline,cate):
    if '-' not in subline:
        return False
    for each in subline.split(','):
        if each.split('-')[1] == '2':
            if sku_info_dic[each.split('-')[0]]['cate'] == cate:
                return True
    return False

total_cate = ['71', '46', '83', '101', '1', '30']
action_weight = {}
action_weight['1'] = 1
action_weight['2'] = 5
action_weight['3'] = 15

#[1, 2, 4, 7, 12, 20, 33, 54, 88]
def Build_feature(idx, line):
    idx=idx+1
    datelist = [0 ,1, 2, 4, 7, 12, 20, 33, 54, 88]
    out = []
    for i in range(1,len(datelist)):
        out.extend(build_feature(line[idx - datelist[i]:idx-datelist[i-1]]))
    return out

def build_feature(seq):
    outnumpy = np.zeros(sku_len)
    for i in range(len(seq)):
        if seq[i] == "0":
            each_feature = np.zeros(sku_len)
        else:
            each_feature = np.zeros(sku_len)
            for each_sku in seq[i].split(','):
                each_sku = each_sku.split('-')
                each_feature += sku_feature[each_sku[0]]*action_weight[each_sku[1]]
        outnumpy += each_feature
    return outnumpy.tolist()


def lastpurchase_cate(idx, line):
    for i in range(idx, 0, -1):
        if have_purchase(line[i]):
            return (idx - i)/365
    return 1

def lastpurchase_all(idx,line):
    out={}
    for cate in total_cate:
        out[cate] = 1
        for i in range(idx,0,-1):
            if have_purchase_spe(line[i],cate):
                out[cate]=(idx-i)/365
                break
    out1=[]
    for key in total_cate:
        out1.append(out[key])
    return out1

def lastwatch_all(idx,line):
    out={}
    for cate in total_cate:
        out[cate] = 1
        for i in range(idx,0,-1):
            if have_watch_spe(line[i],cate):
                out[cate]=(idx-i)/365
                break
    out1=[]
    for key in total_cate:
        out1.append(out[key])
    return out1


def lastoverview_all(idx,line):
    out={}
    for cate in total_cate:
        out[cate] = 1
        for i in range(idx,0,-1):
            if have_overview_spe(line[i],cate):
                out[cate]=(idx-i)/365
                break
    out1=[]
    for key in total_cate:
        out1.append(out[key])
    return out1


def find_object_cate(line):
    out = []
    n = 0
    for i in line:
        if have_purchase(i):
            out.append(n)
        n += 1
    return out

next(user_action_seq)
line=user_action_seq.readline()
n=0
feature_pre=0

while line!="":
    line = line.replace("\n", "").rstrip('\t').split("\t")
    # 建立用户购买目标品类的日期list
    idx = 365
    windows_feature = [random.random()]
    windows_feature.append(lastpurchase_cate(idx, line))
    # 所有类别的上一次购买时间
    windows_feature.extend(lastpurchase_all(idx, line))

    # 所有类别的上一次浏览时间
    windows_feature.extend(lastoverview_all(idx, line))

    # 所有类别的上一次关注时间
    windows_feature.extend(lastwatch_all(idx, line))

    windows_feature.extend(user_feature[line[0]].tolist())
    windows_feature.extend(Build_feature(idx, line))
    a_feature = [int(line[0])]
    a_feature.extend(windows_feature)
    try:
        feature_pre[n] = np.array(a_feature)
    except:
        print('跳入错误')
        feature_pre = np.zeros((98924, len(a_feature)))
        feature_pre[n] = np.array(a_feature)
    n += 1
    if n%1000==0:
        print(a_feature)
        print(feature_pre.shape)
    line = user_action_seq.readline()
np.save("../JDATA用户购买时间预测_A榜/feature_predict_5.npy",feature_pre)
