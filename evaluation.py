import os
import sys
import math

if __name__=='__main__':
    father=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
    
    date={}
    n=0
    for each in open(father+'/JDATA用户购买时间预测_A榜/datefile.txt','r',encoding='utf-8').readline().replace('\n','').split(','):
        date[each]=n
        n+=1

    stand={}
    for line in open(father+'/JDATA用户购买时间预测_A榜/'+sys.argv[2],'r',encoding='utf-8'):
        line=line.replace('\n','').split(',')
        stand[line[0]]=line[1]

    w=0
    W=0
    num=1
    f=0
    s1=1
    s2=1
    for line in open(father+'/JDATA用户购买时间预测_A榜/'+sys.argv[1],'r',encoding='utf-8').readlines():
        line=line.replace('\n','').split(',')
        W+=1/(1+math.log(num))
        if stand[line[0]]=='-1' or line[1]=='-1':
            num+=1
            s1=w/W
            s2=f/(num)
            print('XXXXXXXXXXXXXXX'+'\t'+'0'+'\t'+str(0.4*s1+0.6*s2))
            continue
#        if line[1]==stand[line[0]]:
#            w+=1/(1+math.log(num))
#            f+=1
#            s1=w/W
#            s2=f/(num)
#            num+=1
#            print(line,'rrrrrrrrrrrrrrrr'+'\t'+str(1/(1+math.log(num))+1)+'\t'+str(0.4*s1+0.6*s2))
        else:
            w+=1/(1+math.log(num))
            f+=10/(10+math.pow(abs(date[stand[line[0]]]-date[line[1]]),2))
            s1=w/W
            s2=f/(num)
            num+=1
            print(line[0],line[1],stand[line[0]]+'\t'+str(10/(10+math.pow(abs(date[stand[line[0]]]-date[line[1]]),2)))+'\t'+str(0.4*s1+0.6*s2))
        s1=w/W
        s2=f/(num-1)
    print(s1,s2)
    print(0.4*s1+0.6*s2)

    



