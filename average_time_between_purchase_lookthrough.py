#试图计算每个用户在产生购买行为时，和他上一次浏览该商品之间的时间长度
import os
father=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
user_action_seq=open(father+"/JDATA用户购买时间预测_A榜/user_action_seq.txt","r",encoding="utf-8")
sku_info_dic=eval(open(father+"/JDATA用户购买时间预测_A榜/sku_basic_info_dic.txt","r",encoding="utf-8").read())

next(user_action_seq)
line=user_action_seq.readline()
days=[]
def weatherin(id,line):
	if line=="0":
		return False
	cates=[sku_info_dic[i.split("-")[0]]["cate"] for i in line.split(",")]
	if sku_info_dic[id]["cate"] in cates:
		return True
	else:
		return False
	


while line!="":
	line=line.split("\t")
	for idx in range(len(line)):
		line[idx]=line[idx].split(",")
		for i in line[idx]:
			if "-100" in i:
				id=i.split("-")[0]
				for ii in range(idx-1,-1,-1):
			#		if id in ",".join(line[ii]):
					if weatherin(id,",".join(line[ii])):
						if idx-ii<60:
						#	print(line[0],id, ",".join(line[ii]), idx , ii)
							days.append(idx-ii)
							break
						# print(idx-ii)
	line=user_action_seq.readline()
print(sum(days)/len(days))
# 浏览相同商品13天 浏览同类商品 11.6天
