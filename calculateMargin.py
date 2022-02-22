from findBallotChange import findBallotChange
def findq(Lv,Lc,a,b):
    cnta = 0
    cntb = 0
    qmin = 0
    qmax = 0
    for (c,v) in zip(Lc,Lv):
        if(c == "A"):
            cnta += 1
            if(cnta == a):
                qmax = Lv[v]
        elif(c == "B"):
            cntb += 1
            if(cntb == b):
                qmin = Lv
    return qmin,qmax

def calculateMargin(Lv,Lc,ia,ib,a,b,aq,bq):
    qmin,qmax = findq(Lv,Lc,a,b)
    B1, U, D = findBallotChange(Lv,Lc,ia,ib,qmax,a,b,aq,bq)
    B2, U, D = findBallotChange(Lv, Lc, ia, ib, qmin, a, b, aq, bq)
    B, Umax, Dmin = findBallotChange(Lv,Lc,ia,ib,qmax-1,a,b,aq,bq)
    B, Umin, Dmax = findBallotChange(Lv, Lc, ia, ib, qmin+1, a, b, aq, bq)
    if Dmin > Umax:
        B3 = Dmin
    elif Dmin < Umin and Dmax < Umin:
        B3 = Umin
    else:
        if Dmin < Umin and Dmax < Umin: B3 = Umin
        if Dmin < Umin and Dmax > Umin:
            qleft = qmax - 1
            qright = qmin + 1
            while qleft - qright > 0:
                q = (qleft + qright)/2
                Bq, Uq, Dq = findBallotChange(Lv,Lc,ia,ib,q,a,b,aq,bq)
                if Dq < Uq:
                    qleft = q
                else:
                    qright = q
                if qleft - qright == 1:
                    Bql, Uql, Dql = findBallotChange(Lv, Lc, ia, ib, qleft, a, b, aq, bq)
                    Bqr, Uqr, Dqr = findBallotChange(Lv, Lc, ia, ib, qright, a, b, aq, bq)
                    B3 = min(Bql,Bqr)
    margin = min(min(B1,B2),B3)
    return margin



def findq_multi(Lv,Lc,quotas):
    group_count = [0 for i in quotas]
    qmin = 0
    qmax = 0
    for (c,v) in zip(Lc,Lv):
        group_count[c] += 1
        if qmax == 0 and group_count[c] == quotas[c]:
            qmax = v
        if qmax != 0 and group_count[c] == quotas[c]:
            qmin = v
    return qmin,qmax





def calculateMargin_multigroup(Lv,Lc,I,Quotas,QGroups):
    margin = 0

    return margin


