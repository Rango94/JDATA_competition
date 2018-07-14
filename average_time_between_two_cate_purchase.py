#计算用户两次目标品类购买之间的平均时间
import os
import my_dic
father=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))

user_action_seq=open(father+"/JDATA用户购买时间预测_A榜/user_action_seq.txt","r",encoding="utf-8")

sku_info=my_dic.sku_info_dic

def havedate(subline):
    for each in subline.split(','):
        if sku_info[each.split('-')[0]]['cate']=='101' or sku_info[each.split('-')[0]]['cate']=='30':
            return True
    return False

days=[]
next(user_action_seq)
line=user_action_seq.readline()
while line!="":
	line=line.replace('\n','').split("\t")
	for idx in range(len(line)):
		if "-100" in line[idx] and havedate(line[idx]):
			for i in range(idx-1,-1,-1):
				if "-100" in line[i] and havedate(line[idx]):
					days.append(idx-i)
					break
	line=user_action_seq.readline()
print(sum(days)/len(days))
#31
