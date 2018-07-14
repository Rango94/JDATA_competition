#试图建立一个用户行为序列表，每一行代表用户这一年来的行为，每一列是当天所有用户的行为
#98924个用户id从1到98924
import numpy as np
import os
father=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
user_action=open(father+"/JDATA用户购买时间预测_A榜/jdata_user_action.csv","r",encoding="utf-8")
user_order=open(father+"/JDATA用户购买时间预测_A榜/jdata_user_order.csv","r",encoding="utf-8")
datefile=open(father+"/JDATA用户购买时间预测_A榜/datefile.txt","r",encoding="utf-8")


outfile=open(father+"/JDATA用户购买时间预测_A榜/user_action_seq.txt","w",encoding="utf-8")

def readdate(date):
	date=date.readline().rstrip(",").replace("\n","").split(",")
	dic={}
	for i in range(len(date)):
		dic[date[i]]=i+1
	return date,dic
user_action_seq=np.zeros(shape=(98925,366)).tolist()

for i in range(len(user_action_seq)):
	for j in range(len(user_action_seq[i])):
		user_action_seq[i][j]="0"
#user_action_seq[0,0]="0"

Date,date_dic=readdate(datefile)
user_action_seq[0][1:]=np.array(Date)
for i in range(98924):
	user_action_seq[i+1][0]=i+1

line=user_action.readline()
line=user_action.readline()
while line!="":
	line=line.replace("\n","").split(",")
	id=int(line[0])
	sku_id=line[1]
	date=line[2]
	action=line[4]
	if action=="":
		print("真的有空的！")
	if user_action_seq[id][date_dic[date]]!="0":
		user_action_seq[id][date_dic[date]]+=sku_id+"-"+action+","
	else:
		user_action_seq[id][date_dic[date]]=sku_id+"-"+action+","
	line=user_action.readline()
	
line=user_order.readline()
line=user_order.readline()
while line!="":
	line=line.replace("\n","").split(",")
	id=int(line[0])
	sku_id=line[1]
	date=line[3]
	action="3"
	if user_action_seq[id][date_dic[date]]!="0":
		user_action_seq[id][date_dic[date]]+=sku_id+"-"+action+","
	else:
		user_action_seq[id][date_dic[date]]=sku_id+"-"+action+","
	line=user_order.readline()


for i in user_action_seq:
	for j in i:
		outfile.write(str(j).rstrip(",")+"\t")
	outfile.write("\n")
outfile.close()
#np.save("user_action_seq.npy",user_action_seq)






