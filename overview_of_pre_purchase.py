#想看一下用户在进行购买行为前一个月的行为序列
import os
father=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
user_action_seq=open(father+"/JDATA用户购买时间预测_A榜/user_action_seq.txt","r",encoding="utf-8")
outfile=open(father+"/JDATA用户购买时间预测_A榜/overview_of_pre_purchase.txt","w",encoding="utf-8")
line=user_action_seq.readline()
line=user_action_seq.readline()
while line!="":
	line=line.split("\t")
	for i in range(len(line)):
		if ",100" in line[i] or "100," in line[i]:
			outtmp=line[max(0,i-30):i+1]
			for k in outtmp:
				outfile.write(k+"\t")
			outfile.write("\n")
	line=user_action_seq.readline()