import numpy as np

from calculateMargin import calculateMargin_selectTopK
from findBallotChange import *
from calculateMargin import *
from itertools import permutations

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
        portions.append(newFeatureList)
        return
    perm = permutations(attrDict[i])
    for j in perm:
        featureLists.append(j)
        dfs(i + 1, attrDict, k, featureLists, portions)
    return


def cartesianProductCreatorDiverseTopK(Lv, Lc, portion, k):
    newLc = []
    attrDict = [[] for i in portion]
    for index, i in enumerate(portion):
        for j in i.keys():
            for o in range(i[j]):
                attrDict[index].append(j)
    portions = []
    dfs(0, attrDict, k, [], portions)
    for i, j in zip(Lv, Lc):
        newAttribute = tuple(j)
        newLc.append(newAttribute)
    return newLc, portions


def cartesianProductCreatorBallotChange(Lc, portion, k):
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


def cartesianProductDiverseTopK(Lv, Lc, K, portion):
    newLc, newPortions = cartesianProductCreatorDiverseTopK(Lv, Lc, portion, K)
    best_ballot_change = int('inf')
    for portion in newPortions:
        newPortion = {}
        for i in portion:
            if i in newPortion:
                newPortion[i] += 1
            else:
                newPortion[i] = 1
        ballot_change = calculateMargin_selectTopK(Lv, newLc, K, newPortion)
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


def findBallotChangeMultiMore(Lv, Lc, k, portion, t):
    n = len(Lv)
    # calculate weights
    D_cost = []
    U_cost = []
    for v in Lv:
        if (v >= t):
            D_cost.append(v - t + 1)
            U_cost.append(0)
        else:
            D_cost.append(0)
            U_cost.append(t - v)

    # define model
    model = gp.Model("margin")

    # add variables
    x = model.addVars(n, vtype=GRB.BINARY, name='x')
    u = model.addVar(vtype=GRB.INTEGER, name='u')
    d = model.addVar(vtype=GRB.INTEGER, name='d')
    z = model.addVar(vtype=GRB.INTEGER, name='z')

    # add constraints
    model.addConstr(gp.quicksum(x[i] for i in range(n)) == k)
    for group, value in portion.items():
        model.addConstr(gp.quicksum(x[i] * Lc[i].count(group) for i in range(n)) == value)
    model.addConstr(u == gp.quicksum(x[i] * U_cost[i] for i in range(n)))
    model.addConstr(d == gp.quicksum((1 - x[i]) * D_cost[i] for i in range(n)))
    model.addGenConstrMax(z, [u, d])

    # optimize
    model.setObjective(z, GRB.MINIMIZE)
    model.optimize()

    # output
    # for v in model.getVars():
    #     print(v)
    ballotChange = model.objVal
    return ballotChange
