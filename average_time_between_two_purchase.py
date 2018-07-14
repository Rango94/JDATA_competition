#计算用户两次购买之间的平均时间
import os
father=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))

user_action_seq=open(father+"/JDATA用户购买时间预测_A榜/user_action_seq.txt","r",encoding="utf-8")

days=[]
next(user_action_seq)
line=user_action_seq.readline()
while line!="":
	line=line.split("\t")
	for idx in range(len(line)):
		if "-100" in line[idx]:
			for i in range(idx-1,-1,-1):
				if "-100" in line[i]:
					days.append(idx-i)
					break
	line=user_action_seq.readline()
print(sum(days)/len(days))
#29.72					
