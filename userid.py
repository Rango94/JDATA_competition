#整理所有用户的id
user_action=open("C:/Users/wangnanzhi/Downloads/JDATA用户购买时间预测_A榜/jdata_user_action.csv","r",encoding="utf-8")
line=user_action.readline()
line=user_action.readline()
while line!="":
	line=line.split(",")
	
	line=user_action.readline()
