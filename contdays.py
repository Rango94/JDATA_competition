import os
father=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
user_action=open(father+"/JDATA用户购买时间预测_A榜/jdata_user_action.csv","r",encoding="utf-8")
datafile=open(father+"/JDATA用户购买时间预测_A榜/datefile.txt","w",encoding="utf-8")
line=user_action.readline()
line=user_action.readline()
dic={}
while line!="":
	line=line.split(",")
	if line[2]!="":
		dic[line[2]]=1
	line=user_action.readline()
d = sorted(dic.keys())
for i in d:
	datafile.write(i+",")
datafile.close()
