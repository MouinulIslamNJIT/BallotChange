from findBallotChange import *
import numpy as np
from array import *
import gurobipy as gp
from gurobipy import GRB
import math
from multiAttributesBallotChange import *


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
    # print(Umax,Umin)
    # print(Dmax,Dmin)
    B3 = 0
    # print(Dmin,Umin)
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
    group_count = [0 for i in portions]
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
    B3 = 1000000
    q = -1
    if Dmin > Umax:
        print('Dmin')
        B3 = Dmin
    elif Dmin < Umin and Dmax < Umin:
        print('Umin')
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
    C = [0 for i in portion]
    slack = k - sum([np.floor(i) for i in portion])
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


def AlgOptMFMultiMore(Lv, Lc, k, portions):
    margin = 10000000
    Opt_t = -1
    for t in range(min(Lv), max(Lv) + 1):
        b = findBallotChangeMultiMore(Lv, Lc, k, portions, t)
        if margin > b:
            margin = b
            Opt_t = t
    return margin, Opt_t



def findMarginLexi(Lv, Lc, LeximinTopk,k):
    #create new Lc
    # if candidate comes form leximin output assign them 0, otherwise assign 1
    for i in range(len(Lc)):
        if i in LeximinTopk:
            Lc[i] = 0
        else:
            Lc[i] = 1

    #because we want all from leximin output in top-k.
    a = [k,0]

    #iterate all q using findBallotChange
    margin = 10000000
    for q in range(min(Lv),max(Lv)+1):
        Bq, Uq, Dq = FindBallotChangeMulti(Lv, Lc, a, q)
        if margin > Bq:
            margin = Bq
    print(margin)
    return margin