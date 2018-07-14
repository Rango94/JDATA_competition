#建立商品属性和消费者的信息字典，以便后续程序使用
import os
father=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
sku_basic_info=open(father+"/JDATA用户购买时间预测_A榜/jdata_sku_basic_info.csv","r",encoding="utf-8")
user_basic_info=open(father+"/JDATA用户购买时间预测_A榜/jdata_user_basic_info.csv","r",encoding="utf-8")
user_action_seq=open(father+"/JDATA用户购买时间预测_A榜/user_action_seq.txt","r",encoding="utf-8")


def have_purchase(subline):
    if '-' not in subline:
        return False
    for each in subline.split(','):
        if each.split('-')[1]=='3':
            if sku_basic_info_dic[each.split('-')[0]]['cate']=='101' or sku_basic_info_dic[each.split('-')[0]]['cate']=='30':
                return True
    return False


def cont_complex_gap(first_action,line):
    total_cate=['71', '46', '83', '101', '1', '30']
    object_cate=['101', '30']
    if first_action=='overview':
        first_action='-1'
    if first_action=='watch':
        first_action='-2'
    if first_action=='purchase':
        first_action='-3'
    out_list=[]
    for one_of_tc in total_cate:
        for one_of_oc in object_cate:
            total_cate_list=[]
            object_cate_list=[]
            for idx in range(len(line)):
                for each in line[idx].split(','):
                    if first_action in each and one_of_tc == sku_basic_info_dic[each.split('-')[0]]['cate']:
                        total_cate_list.append(idx)
                for each in line[idx].split(','):
                    if  '-3' in each and one_of_oc ==sku_basic_info_dic[each.split('-')[0]]['cate']:
                        object_cate_list.append(idx)
            total_cate_list.reverse()
            object_cate_list.reverse()
            gap_list=[]
            for i in object_cate_list:
                for j in total_cate_list:
                    if j <i :
                        gap_list.append(i-j)
                        break
            if len(gap_list)==0:
                out_list.append(365)
            else:
                out_list.append(sum(gap_list)/len(gap_list))
    # print(out_list)
    return out_list



sku_basic_info_dic={}
next(sku_basic_info)
line=sku_basic_info.readline()
while line!="":
    line=line.replace("\n","").split(",")
    tmp_dic={}
    tmp_dic["price"]=line[1]
    tmp_dic["cate"]=line[2]
    tmp_dic["para_1"]=line[3]
    tmp_dic["para_2"]=line[4]
    tmp_dic["para_3"]=line[5]
    sku_basic_info_dic[line[0]]=tmp_dic
    line=sku_basic_info.readline()

user_basic_info_dic={}
next(user_basic_info)
line=user_basic_info.readline()
while line!="":
    line=line.replace("\n","").split(",")
    tmp_dic={}
    tmp_dic["age"]=line[1]
    tmp_dic["sex"]=line[2]
    tmp_dic["user_lv_cd"]=line[3]
    user_basic_info_dic[line[0]]=tmp_dic
    line=user_basic_info.readline()



next(user_action_seq)
line=user_action_seq.readline()
while line!="":
    # 计算每个用户的平均购买间隔
    user_tmp_dic=[]
    times=0
    line=line.replace("\n","").split("\t")
    start=0
    end=0
    for idx in range(len(line)):
        if "-3" in line[idx]:
            start=idx
            break
    for idx in range(len(line)-1,-1,-1):
        if '-3' in line[idx]:
            end=idx
            break
    for idx in range(start,end):
        if '-3' in line[idx]:
            times+=1
    if end==start:
        user_basic_info_dic[line[0]]['purchase_gap']=365
    else:
        user_basic_info_dic[line[0]]["purchase_gap"]=(end-start)/times

    # 计算每个用户对目标品类的平均购买间隔
    times=0
    start=0
    end=0
    for idx in range(len(line)):
        if have_purchase(line[idx]):
            start=idx
            break
    for idx in range(len(line)-1,-1,-1):
        if have_purchase(line[idx]):
            end=idx
            break
    for idx in range(start,end):
        if have_purchase(line[idx]):
            times+=1
    if end==start:
        user_basic_info_dic[line[0]]['cate_purchase_gap']=365
    else:
        user_basic_info_dic[line[0]]["cate_purchase_gap"]=(end-start)/times
    # print(user_basic_info_dic[line[0]]["cate_purchase_gap"])

    #所有商品的浏览购买比,关注购买比
    purchase_list=[]
    overview_list=[]
    wathch_list=[]
    for idx in range(len(line)):
        for i in line[idx].split(','):
            if '-1' in i:
                overview_list.append(sku_basic_info_dic[i.split('-')[0]]['cate'])
            if '-2' in i:
                wathch_list.append(sku_basic_info_dic[i.split('-')[0]]['cate'])
            if '-3' in i:
                purchase_list.append(sku_basic_info_dic[i.split('-')[0]]['cate'])

    #浏览购买比
    try:
        user_basic_info_dic[line[0]]["purchase/overview"] = len(purchase_list)/len(overview_list)
    except:
        user_basic_info_dic[line[0]]["purchase/overview"] = 0
    watch_times = 0
    for i in purchase_list:
        if i in wathch_list:
            watch_times+=1
    #关注购买比
    if len(wathch_list)==0:
        user_basic_info_dic[line[0]]["purchase/watch"]=0
    else:
        user_basic_info_dic[line[0]]["purchase/watch"]=watch_times/len(wathch_list)

    '''
      浏览X商后购买Y商品的平均间隔
      关注X商后购买Y商品的平均间隔
      购买X商后购买Y商品的平均间隔
      X属于['71', '46', '83', '101', '1', '30'] 
      Y属于['101','30']
    '''

    first_action = ['overview', 'watch', 'purchase']
    for action in first_action:
        ac_num=1
        for i in cont_complex_gap(action,line):
            user_basic_info_dic[line[0]][action+'_gap_'+str(ac_num)] = i
            ac_num+=1

    '''
    用户对于以上种类商品的浏览，关注，购买量3*6=18
    '''
    total_cate = ['71', '46', '83', '101', '1', '30']
    sku_num=[{'71':0,'46':0,'83':0,'101':0,'1':0,'30':0},{'71':0,'46':0,'83':0,'101':0,'1':0,'30':0},{'71':0,'46':0,'83':0,'101':0,'1':0,'30':0}]
    # sku_num_watch={'71':0,'46':0,'83':0,'101':0,'1':0,'30':0}
    # sku_num_purchase = {'71': 0, '46': 0, '83': 0, '101': 0, '1': 0, '30': 0}
    for subline in line:
        if '-' in subline:
            for each in subline.split(','):
                each=each.split('-')
                if each[1]=='1':
                    sku_num[0][sku_basic_info_dic[each[0]]['cate']]+=1
                if each[1]=='2':
                    sku_num[1][sku_basic_info_dic[each[0]]['cate']]+=1
                if each[1]=='3':
                    sku_num[2][sku_basic_info_dic[each[0]]['cate']]+=1


    for sub in range(len(sku_num)):
        for key in total_cate:
            user_basic_info_dic[line[0]][first_action[sub]+'_num_'+key]=sku_num[sub][key]
            # print(user_basic_info_dic[line[0]][first_action[sub]+'_'+key],'\t',end='')
    # print()







    #用户平均购买商品的价格
    price_list=[]
    for subline in line:
        if '-' in subline:
            for each in subline.split(','):
                if '-3' in each:
                    price_list.append(float(sku_basic_info_dic[each.split('-')[0]]['price']))
    user_basic_info_dic[line[0]]['average_price']=sum(price_list)/len(price_list)
    if int(line[0])%1000==0:
        print(line[0])

    line=user_action_seq.readline()


out_sku_basic_info=open(father+"/JDATA用户购买时间预测_A榜/sku_basic_info_dic.txt","w",encoding="utf-8")
out_user_basic_info=open(father+"/JDATA用户购买时间预测_A榜/user_basic_info_dic.txt","w",encoding="utf-8")

out_sku_basic_info.write(str(sku_basic_info_dic))
out_user_basic_info.write(str(user_basic_info_dic))

out_sku_basic_info.close()
out_user_basic_info.close()
