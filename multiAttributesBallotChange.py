import numpy as np
from calculateMargin import diverse_top_k, calculateMargin_multigroup
from findBallotChange import *
from itertools import permutations
import copy
from array import *
import gurobipy as gp
from gurobipy import GRB
import math


def dfs(i, attrDict, k, featureLists, portions):
    if i >= len(attrDict):
        newFeatureList = []
        for x in range(k):
            newFeature = []
            for y in featureLists:
                newFeature.append(y[x])
            newFeatureList.append(tuple(newFeature))
        portions.add(tuple(newFeatureList))
        return
    perm = permutations(attrDict[i])
    for j in perm:
        featureLists.append(j)
        dfs(i + 1, attrDict, k, featureLists, portions)
        featureLists.pop()
    return

def cartesianProductCreatorDiverseTopK(Lc, portion, k):
    newLc = []
    attrDict = [[] for i in portion]
    for index, i in enumerate(portion):
        for j in i.keys():
            for o in range(i[j]):
                attrDict[index].append(j)
    portions = set()
    dfs(0, attrDict, k, [], portions)
    portions = list(portions)
    for i in Lc:
        newAttribute = tuple(i)
        newLc.append([i[0], newAttribute])
    return newLc, portions


def cartesianProductCreatorBallotChange(Lc, portion, k):
    newLc = []
    attrDict = [[] for i in portion]
    for index, i in enumerate(portion):
        for j in i.keys():
            for o in range(i[j]):
                attrDict[index].append(j)
    portions = set()
    dfs(0, attrDict, k, [], portions)
    portions = list(portions)
    for i in Lc:
        newAttribute = tuple(i)
        newLc.append(newAttribute)
    return newLc, portions


def allNewFeatures(i,portion,curF,newFeatures):
    if i >= len(portion):
        newFeatures[tuple(curF)] = 0
        return
    for j in portion[i]:
        curF.append(j)
        allNewFeatures(i+1,portion,curF,newFeatures)
        curF.pop()
    return

def calculateMargin_selectTopK(Lv,Lc, K, portion):
    new_portion = diverse_top_k(Lv,Lc, K, portion)
    margin = calculateMargin_multigroup(Lv, Lc, new_portion)
    return margin

def checkPortion(newLc,newPortion):
    Lcfreq = {}
    for i in newLc:
        Lcfreq.setdefault(i,0)
        Lcfreq[i]+=1

    for i in newPortion.keys():
        if newPortion[i] > 0:
            if i not in Lcfreq:
                return False
            elif newPortion[i] > Lcfreq[i]:
                return False
    return True



def cartesianProductDiverseTopK(Lv, Lc, K, portion):
    newLc, newPortions = cartesianProductCreatorBallotChange(Lc, portion, K)
    best_ballot_change = 100000000
    newFeatures = {}
    allNewFeatures(0,portion,[],newFeatures)
    for portion in newPortions:
        new_portion = copy.deepcopy(newFeatures)
        for i in portion:
            new_portion[i] += 1
        if checkPortion(newLc, new_portion):
            ballot_change = calculateMargin_selectTopK(Lv, newLc, K, new_portion)
            best_ballot_change = min(ballot_change, best_ballot_change)
    return best_ballot_change



def cartesianProductDiverseTopKIndep(Lv, Lc, K, portion):
    newLc, newPortions = cartesianProductCreatorBallotChange(Lc, portion, K)
    best_ballot_change = float('inf')
    newFeatures = {}
    allNewFeatures(0,portion,[],newFeatures)
    #portion = np.random.choice(newPortions,1)[0]
    portion = newPortions[np.random.randint(len(newPortions))]
    new_portion = copy.deepcopy(newFeatures)
    for i in portion:
        new_portion[i] += 1
    if checkPortion(newLc, new_portion):
        ballot_change = calculateMargin_selectTopK(Lv, newLc, K, new_portion)
        best_ballot_change = min(ballot_change, best_ballot_change)
    return best_ballot_change



def cartesianProductMargin(Lv, Lc, k, portion):
    newLc, newPortions = cartesianProductCreatorBallotChange(Lc, portion, k)
    best_ballot_change = float('inf')
    newFeatures = {}
    allNewFeatures(0,portion,[],newFeatures)
    for x in newPortions:
        new_portion = copy.deepcopy(newFeatures)
        for i in x:
            new_portion[i] += 1
        if checkPortion(newLc,new_portion):
            # Lcdict = {}
            # idxLc = []
            # for idx,group in enumerate(set(new_portion.keys())):
            #     Lcdict[group] = idx
            # for group in newLc:
            #     idxLc.append(Lcdict[group])
            # print(len(new_portion.values()), max(idxLc), len(Lv))
            ballot_change = calculateMargin_multigroup(Lv, newLc, new_portion)
            best_ballot_change = min(ballot_change, best_ballot_change)
    return best_ballot_change


