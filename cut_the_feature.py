import os
import numpy as np
import sys
import random
father=os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
feature=open(father+"/JDATA用户购买时间预测_A榜/third_feature_4_all.txt.sort",'r',encoding='utf-8')
#5632890

if __name__=='__main__':
    innum=int(sys.argv[1])
    total=int(sys.argv[2])
    next(feature)
    len_=len(feature.readline().rstrip().split('\t'))
    outfeature=np.zeros((innum,len_))
    g=int((innum/total)*100)
    n=0
    for i in range(total):
        line=feature.readline()
        if i%100<g and n<innum:
            try:
                outfeature[n]=np.array([float(i) for i in line.rstrip().split('\t')])
            except:
                continue
            n+=1
    print(len(outfeature))
    need_delete=[]
    for i in range(len(outfeature)):
        if sum(outfeature[i])==0:
            need_delete.append(i)
    outfeature=np.delete(outfeature,need_delete,0)
    print(len(outfeature))
    np.save(father+"/JDATA用户购买时间预测_A榜/sub_third_feature.npy",outfeature)

