#第二次尝试提取用户序列特征
import os
import my_dic
import numpy as np
import random
father=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))

user_action_seq=open(father+"/JDATA用户购买时间预测_A榜/user_action_seq.txt","r",encoding="utf-8")
feature_head=open(father+"/JDATA用户购买时间预测_A榜/sec_feature_all.txt","w",encoding="utf-8")
feature_head.write('#第一列是label 第二列是下次购买时间，第三列是目标品类平均购买间隔，第四列上一次购买日期，第五列是窗口日期'+'\n')

sku_info_dic=my_dic.sku_info_dic
user_info_dic=my_dic.user_info_dic

sku_feature=my_dic.sku_feature_dic
user_feature=my_dic.user_feature_dic

sku_len=len(sku_feature['1'])
user_len=len(user_feature['1'])

#为了更好的保存用户对商品的行为特征，我们不能对浏览和关注取one-hot，所以这里设浏览权重为1，关注权重为3,购买权重为10

def have_purchase(subline):
    if '-' not in subline:
        return False
    for each in subline.split(','):
        if each.split('-')[1]=='100':
            if sku_info_dic[each.split('-')[0]]['cate']=='101' or sku_info_dic[each.split('-')[0]]['cate']=='30':
                return True
    return False


action_weight={}
action_weight['1']=0
action_weight['2']=sku_len
action_weight['100']=sku_len*2

def Build_feature(idx,line):
    datelist=[1,3,5,7,14,21,28,35]
    out=[]
    for i in datelist:
        out.extend(build_feature(line[idx-i:idx]))
    return out

def build_feature(seq):
    outnumpy=np.zeros(sku_len*3)
    for i in range(len(seq)):
        if seq[i]=="0":
            each_feature=np.zeros(sku_len*3)
        else:
            each_feature=np.zeros(sku_len*3)
            for each_sku in seq[i].split(','):
                each_sku=each_sku.split('-')
                try:
                    each_feature[action_weight[each_sku[1]]:action_weight[each_sku[1]]+sku_len]+=sku_feature[each_sku[0]]
                except:
                    print(each_sku)
        outnumpy+=each_feature
    return outnumpy.tolist()

def lastpurchase(idx,line):
    for i in range(idx+30,0,-1):
        if have_purchase(line[i]):
            return idx+30-i
    return 365
    
def find_object_cate(line):
    out=[]
    n=0
    for i in line:
        if have_purchase(i):
            out.append(n)
        n+=1
    return out

next(user_action_seq)
line=user_action_seq.readline()

n=0
while line!="":
    line=line.replace("\n","").rstrip('\t').split("\t")
    #建立用户购买目标品类的日期list
    date_idx=find_object_cate(line)
    for k in date_idx:
        if k<36:
            continue
    #在购买目标品类的日期周围随机取相应特征15次
        for ll in range(15):
            idx=random.randint(max(k-65,1),k-35)
            windows_feature=[float(user_info_dic[line[0]]['cate_gap'])/365,lastpurchase(idx,line)/365,idx/365]
            windows_feature.extend(user_feature[line[0]].tolist())
            windows_feature.extend(Build_feature(idx+35,line))
            gap=-1
    #计算下一次购买时间
            for i in range(idx+35,min(idx+66,365)):
                gap=-1
                if have_purchase(line[i]):
                    gap=i-idx-34
                  #  print(i,idx,gap)
                    break
#第一列是用户id，第二列是label(下次购买的间隔)，第三列是目标品类平均购买间隔，第四列是上一次购买日期，第五列是窗口日期
            a_feature=[gap]
            a_feature.extend(windows_feature)
            feature_head.write(line[0]+'\t')
            for a in a_feature:
                feature_head.write('%.4f'%a+"\t")
            feature_head.write('\n')
    for ll in range(15):
        idx=random.randint(1,290)
        windows_feature=[float(user_info_dic[line[0]]['cate_gap'])/365,lastpurchase(idx,line)/365,idx/365]
        windows_feature.extend(user_feature[line[0]].tolist())
        windows_feature.extend(Build_feature(idx+35,line))
        gap=-1
    #计算下一次购买时间
        for i in range(idx+35,min(idx+66,365)):
            gap=-1
            if have_purchase(line[i]):
                gap=i-idx-34
                break
#第一列是用户id，第二列是label(下次购买的间隔)，第三列是目标品类平均购买间隔，第四列是上一次购买日期，第五列是窗口日期
        a_feature=[gap]
        a_feature.extend(windows_feature)
        feature_head.write(line[0]+'\t')
        for a in a_feature:
            feature_head.write('%.4f'%a+"\t")
        feature_head.write('\n')
    n+=1
    line=user_action_seq.readline()
