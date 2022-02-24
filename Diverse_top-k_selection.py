import numpy as np
from findBallotChange import *
from calculateMargin import *
def diverse_top_k(I:list[list], K:int, d:list, portion:dict):    #     I contains the all items with their category value;
    topk = []
    Lv =[x[0] for x in I]
    Lc = [x[1] for x in I]
    C = dict.fromkeys(d,0)
    slack = K - sum([np.floor(i) for i in portion.values()])
    iter = 0
    while(len(topk)<K):
        x = I[iter]
        iter += 1
        i = x[1]
        if C[i] < np.floor(portion[i]):
            topk.append(x)
            C[i] += 1
        elif(C[i]<np.ceil(portion[i]) and slack>0):
            topk.append(x)
            C[i] += 1
            slack -= 1
    return Lv,Lc,C

def calculateBallotChange_selectTopK(I:list[list], K:int, d:list, portion:dict):
    Lv,Lc,new_portion = diverse_top_k(I, K, d, portion)
    margin = calculateMargin_multigroup(Lv,Lc,new_portion)
    BallotChange,_,_ = FindBallotChangeMulti(Lv, Lc, new_portion, margin)
    return  BallotChange


def dfs(attrDict,i,portion,featureList:list,curProb,k,newPortion):
    if i >= len(attrDict):
        newPortion[tuple(featureList)] = curProb
        return
    for group in attrDict[i]:
        featureList.append(group)
        curProb *= portion[i][group]/k
        dfs(i+1,portion,featureList,curProb,k,newPortion)
    return



def cartesianProductCreator(I:list[list],portion:list[dict],k:int):
    newItemPortion = 1
    # for index, j in enumerate(i[1:]):
    #     newItemPortion *= portion[index][j] / k
    newI = []
    newPortion = {}
    attrDict = [set(i.keys()) for i in portion]
    dfs(attrDict, 0, portion, [], 1, k, newPortion)
    for i in I:
        newAttribute = tuple(i[1:])
        newI.append([i[0],newAttribute])
    return newI, newPortion,list(newPortion.keys())


def cartesian_product_selectTopK(I:list[list], K:int, d:list, portion:list[dict]):
    newI, newPortion, newD = cartesianProductCreator(I,portion,K)
    ballot_change = calculateBallotChange_selectTopK(newI, K, newD, newPortion)
    return ballot_change

