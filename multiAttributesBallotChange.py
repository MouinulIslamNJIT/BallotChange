import numpy as np
from findBallotChange import *
from calculateMargin import *
from itertools import permutations


def diverse_top_k(I: list[list], K: int, d: list, portion: dict):  # I contains the all items with their category value;
    topk = []
    Lv = [x[0] for x in I]
    Lc = [x[1] for x in I]
    C = dict.fromkeys(d, 0)
    slack = K - sum([np.floor(i) for i in portion.values()])
    iter = 0
    while (len(topk) < K):
        x = I[iter]
        iter += 1
        i = x[1]
        if C[i] < np.floor(portion[i]):
            topk.append(x)
            C[i] += 1
        elif (C[i] < np.ceil(portion[i]) and slack > 0):
            topk.append(x)
            C[i] += 1
            slack -= 1
    return Lv, Lc, C


def calculateBallotChange_selectTopK(I: list[list], K: int, d: list, portion: dict):
    Lv, Lc, new_portion = diverse_top_k(I, K, d, portion)
    margin = calculateMargin_multigroup(Lv, Lc, new_portion)
    BallotChange, _, _ = FindBallotChangeMulti(Lv, Lc, new_portion, margin)
    return BallotChange


def dfs(i, attrDict, k, featureLists, portions):
    if i >= len(attrDict):
        newFeatureList = []
        for x in range(k):
            newFeature = []
            for y in featureLists:
                newFeature.append(y[x])
            newFeatureList.append(tuple(newFeature))
        portions.append(newFeatureList)
        return
    perm = permutations(attrDict[i].keys())
    for j in perm:
        featureLists.append(j)
        dfs(i + 1, attrDict, k, featureLists, portions)
    return


# def dfs(attrDict,i,featureList:list,curProb,k,selected):
#     if i >= len(attrDict):
#         selected.append(tuple(featureList))
#         return
#     for group in attrDict[i]:
#         featureList.append(group)
#         dfs(i+1,featureList,curProb,k,selected)
#     return


def cartesianProductCreatorDiverseTopK(I: list[list], portion: list[dict], k: int):
    newI = []
    attrDict = [[] for i in portion]
    for index, i in enumerate(portion):
        for j in i.keys():
            for o in range(i[j]):
                attrDict[index].append(j)
    portions = []
    dfs(0, attrDict, k, [], portions)
    for i in I:
        newAttribute = tuple(i[1:])
        newI.append([i[0], newAttribute])
    return newI, portions


def cartesianProductCreatorBallotChange(Lv, Lc, portion: list[dict], k: int):
    newLc = []
    attrDict = [[] for i in portion]
    for index, i in enumerate(portion):
        for j in i.keys():
            for o in range(i[j]):
                attrDict[index].append(j)
    portions = []
    dfs(0, attrDict, k, [], portions)
    for i in Lc:
        newAttribute = tuple(i)
        newLc.append([i[0], newAttribute])
    return newLc, portions


def cartesianProductDiverseTopK(I: list[list], K: int, portion: list[dict]):
    newI, newPortions = cartesianProductCreatorDiverseTopK(I, portion, K)
    best_ballot_change = int('inf')
    for portion in newPortions:
        newPortion = {}
        for i in portion:
            if i in newPortion:
                newPortion[i] += 1
            else:
                newPortion[i] = 1
        newD = list(newPortion.keys())
        ballot_change = calculateBallotChange_selectTopK(newI, K, newD, newPortion)
        best_ballot_change = min(ballot_change, best_ballot_change)
    return best_ballot_change


def cartesianProductBallotChange(Lv, Lc, k, portion):
    newLc, newPortions = cartesianProductCreatorBallotChange(Lv, Lc, portion, k)
    best_ballot_change = int('inf')
    for portion in newPortions:
        new_portion = {}
        for i in portion:
            if i in new_portion:
                new_portion[i] += 1
            else:
                new_portion[i] = 1
        ballot_change = calculateMargin_multigroup(Lv, newLc, new_portion)
        best_ballot_change = min(ballot_change, best_ballot_change)
    return best_ballot_change
