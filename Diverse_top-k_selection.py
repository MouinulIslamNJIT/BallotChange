import numpy as np
from findBallotChange import *
from calculateMargin import *
def diverse_top_k(I:list[list], K:int, d:list, quotas:dict):    #     I contains the all items with their category value;
    Lv =[]
    Lc = []
    C = dict.fromkeys(d,0)
    slack = K - sum([np.floor(i) for i in quotas.values()])
    iter = 0
    while(len(Lv)<K):
        x = I[iter]
        iter += 1
        i = x[1]
        if C[i] < np.floor(quotas[i]):
            Lv.append(x[0])
            Lc.append(x[1])
            C[i] += 1
        elif(C[i]<np.ceil(quotas[i]) and slack>0):
            Lv.append(x[0])
            Lc.append(x[1])
            C[i] += 1
            slack -= 1
    return Lv,Lc

def calculateBallotChange(I:list[list], K:int, d:list, quotas:dict):
    Lv,Lc = diverse_top_k(I, K, d, quotas)
    Quotas = []
    QGroups = []
    q = calculateMargin_multigroup(Lv,Lc,I,Quotas,QGroups)
    BallotChange = findBallotChange_multigroups(Lv,Lc,I,q,Quotas,QGroups)
    return  BallotChange



