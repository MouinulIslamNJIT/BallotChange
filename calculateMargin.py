from findBallotChange import *
import numpy as np
from array import *
import gurobipy as gp
from gurobipy import GRB
import math
import random
import networkx as nx



random.seed(0)
np.random.seed(0)
def findq(Lv,Lc,a,b):
    cnta = 0
    cntb = 0
    qmin = 0
    qmax = 0
    for (c,v) in zip(Lc,Lv):
        if(c == "A"):
            cnta += 1
            if(cnta == a):
                qmin = v
        if(c == "B"):
            cntb += 1
            if(cntb == b):
                qmax = v
    return qmin,qmax

def calculateIandQ(Lv,Lc,a,b):
    counta = 0
    countb = 0
    ia = -1
    ib = -1
    aq = -1
    bq = -1
    for (i,j) in zip(enumerate(Lv),Lc):
        if j == "A":
            counta += 1
        if j == "B":
            countb += 1
        if counta == a:
            ia = i[0]
            aq = i[1]
        if countb == b:
            ib = i[0]
            bq = i[1]
    return ia,aq,ib,bq





def calculateMargin(Lv,Lc,a,b):
    qmin,qmax = findq(Lv,Lc,a,b)
    B1, U, D = findBallotChange(Lv,Lc,qmax,a,b,qmin,qmax)
    B2, U, D = findBallotChange(Lv,Lc,qmin,a,b,qmin,qmax)
    B, Umax, Dmin = findBallotChange(Lv,Lc,qmax-1,a,b,qmin,qmax)
    B, Umin, Dmax = findBallotChange(Lv,Lc,qmin+1,a,b,qmin,qmax)
    B3 = 0
    q = -1
    if Dmin > Umax:
        B3 = Dmin
    elif Dmin < Umin and Dmax < Umin:
        B3 = Umin
    else:
        qright = qmax - 1
        qleft = qmin + 1
        while qright - qleft > 0.1:
            q = (qleft + qright)/2
            Bq, Uq, Dq = findBallotChange(Lv,Lc,q,a,b,qmin,qmax)
            if qright - qleft <= 1:
                Bql, Uql, Dql = findBallotChange(Lv,Lc,int(qleft),a,b,qmin,qmax)
                Bqr, Uqr, Dqr = findBallotChange(Lv,Lc,int(qright),a,b,qmin,qmax)
                B3 = min(Bql,Bqr)
            if Dq < Uq:
                qright = q
            else:
                qleft = q
    # print(B1,B2,B3)
    margin = min(min(B1,B2),B3)
    return margin



def findq_multi(Lv,Lc,portions):
    group_count = dict.fromkeys(portions.keys(),0)
    qmin = 0
    qmax = 0
    for (c,v) in zip(Lc,Lv):
        group_count[c] += 1
        if qmax == 0 and group_count[c] == portions[c]:
            qmax = v
        if qmax != 0 and group_count[c] == portions[c]:
            qmin = v
    return qmin,qmax





def calculateMargin_multigroup(Lv,Lc,portions):
    qmin,qmax = findq_multi(Lv, Lc, portions)
    B1, U, D = FindBallotChangeMulti(Lv, Lc, portions,qmax)
    B2, U, D = FindBallotChangeMulti(Lv, Lc, portions,qmin)
    B, Umax, Dmin = FindBallotChangeMulti(Lv,Lc,portions,qmax-1)
    B, Umin, Dmax = FindBallotChangeMulti(Lv,Lc,portions,qmin+1)
    # print(qmin,qmax)
    # print(Umin,Umax)
    # print(Dmin, Dmax)
    B3 = 999999999
    q = -1
    if Dmin > Umax:
        B3 = Dmin
    elif Dmin < Umin and Dmax < Umin:
        B3 = Umin
    else:
        qright = qmax - 1
        qleft = qmin + 1
        while qright - qleft > 0.1:
            q = (qleft + qright)/2
            Bq, Uq, Dq = FindBallotChangeMulti(Lv,Lc,portions,q)
            if qright - qleft <= 1:
                Bql, Uql, Dql = FindBallotChangeMulti(Lv,Lc,portions,int(qleft))
                Bqr, Uqr, Dqr = FindBallotChangeMulti(Lv,Lc,portions,int(qright))
                B3 = min(Bql,Bqr)
            if Dq < Uq:
                qright = q
            else:
                qleft = q

    margin = min(min(B1,B2),B3)
    return margin


def diverse_top_k(Lv,Lc, k, portion):
    # I contains the all items with their category value;
    topk = []
    C = dict.fromkeys(portion.keys(),0)
    slack = k - sum([np.floor(i) for i in portion.values()])
    iter = 0
    # print(slack)
    # print(len(Lc))
    while (len(topk) < k) and iter < len(Lc):
        i = Lc[iter]
        iter += 1
        if C[i] < np.floor(portion[i]):
            C[i] += 1
        elif (C[i] < np.ceil(portion[i]) and slack > 0):
            C[i] += 1
            slack -= 1
    # print(sum(C),k)
    return C



def calculateMargin_selectTopK(Lv,Lc, K, portion):
    new_portion = diverse_top_k(Lv,Lc, K, portion)
    margin = calculateMargin_multigroup(Lv, Lc, new_portion)
    return margin



def findBallotChangeMultiMore(Lv, Lc, a, k, t):
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
    for group, value in a.items():
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



def AlgOptMFMultiMore(Lv, Lc, k, portions):
    margin = float('inf')
    Opt_t = -1
    for t in range(min(Lv), max(Lv) + 1):
        b = findBallotChangeMultiMore(Lv, Lc, portions, k, t)
        if margin > b:
            margin = b
            Opt_t = t
    return margin, Opt_t


def findMarginLexi(Lv, Lc, LeximinTopk,k):
    #create new Lc
    # if candidate comes form leximin output assign them 0, otherwise assign 1
    Lc_new = {}
    for i in Lc:
        Lc_new[i]=0
    for i in Lc:
        if i in LeximinTopk:
            Lc_new[i] = 0
        else:
            Lc_new[i] = 1
    Lc = Lc_new
    #because we want all from leximin output in top-k.
    a = {0:k,1:0}

    #iterate all q using findBallotChange
    margin = float('inf')
    for q in range(min(Lv),max(Lv)+1):
        Bq, Uq, Dq = FindBallotChangeMulti(Lv, Lc, a, q)
        print("ballot sub = ",Bq, Uq, Dq)
        if margin > Bq:
            margin = Bq
    print(margin)
    return margin


def findAplusR(Lv, Lc, a, t, k):
    A = [set(), set()]
    for i, j in Lc:
        A[0].add(i)
        A[1].add(j)
    A = [list(A[0]), list(A[1])]
    # print(A)

    # Find weights:
    w = []
    for i in range(len(Lv)):
        if Lv[i] < t:
            w.append(t - Lv[i])
        else:
            w.append((t - 1) - Lv[i])
    # print(w)

    # initialize graph
    G = nx.DiGraph()

    # Add source and destination
    G.add_node("Source", demand=-k)
    G.add_node("Destination", demand=k)

    for i in range(len(A[0])):
        # print(A[0][i],a[0][A[0][i]])
        G.add_edge("Source", A[0][i], capacity=a[0][A[0][i]])
    for i in range(len(A[1])):
        # print(A[1][i],a[1][A[1][i]])
        G.add_edge(A[1][i], "Destination", capacity=a[1][A[1][i]])

    # Add edges
    dummyWeight = {}
    for c in range(len(Lc)):
        i, j = Lc[c]
        r = random.random()
        dummy = j + "_" + str(r)
        # dummyWeight[dummy] = w[c]
        G.add_edge(i, dummy, weight=w[c], capacity=1)
        G.add_edge(dummy, j, weight=0, capacity=1)

    # solve min cost flow
    flowDict = nx.min_cost_flow(G)
    cost = nx.cost_of_flow(G, flowDict)

    costAR = cost
    for wc in w:
        if wc < 0:
            costAR = costAR - wc
    # print(cost)
    # print(costAR)
    # print(flowDict)
    return costAR

def AlgMFMulti2(Lv,Lc,a,k):
    OPT_ar = float('inf')
    OPT_t = -1
    Lvunq = list(set(Lv))
    Lvunq.reverse()
    #print(Lvunq)
    for i in range(len(Lvunq)):
        #print(Lv[i],Lv[i] + 1,Lv[i+1] - 1)
        cost1 = findAplusR(Lv,Lc,a,Lvunq[i],k)
        cost2 = findAplusR(Lv,Lc,a,Lvunq[i]+1,k)
        #print(i)
        cost3 = 999999999
        ind3 = -1
        if i < len(Lvunq) - 1:
            cost3 = findAplusR(Lv,Lc,a,Lvunq[i+1]-1,k)
            ind3 = Lvunq[i+1]
        cost,t = min((cost1,Lvunq[i]),(cost2,Lvunq[i]+1),(cost3,ind3 - 1))
        #print(cost,t)
        if   cost < OPT_ar:
            OPT_ar = cost
            OPT_t = t
    print (OPT_ar,OPT_t)