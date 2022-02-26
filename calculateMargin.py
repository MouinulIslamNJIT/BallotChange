from findBallotChange import *
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
        qleft = qmax - 1
        qright = qmin + 1
        print(qleft, qright)
        while qleft - qright > 1:
            q = (qleft + qright)/2
            Bq, Uq, Dq = findBallotChange(Lv,Lc,q,a,b,qmin,qmax)
            if Dq < Uq:
                qleft = q
            else:
                qright = q
            if qleft - qright == 1:
                Bql, Uql, Dql = findBallotChange(Lv,Lc,qleft,a,b,qmin,qmax)
                Bqr, Uqr, Dqr = findBallotChange(Lv,Lc,qright,a,b,qmin,qmax)
                B3 = min(Bql,Bqr)
    print(B1,B2,B3)
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
    qmin, qmax = findq_multi(Lv, Lc, portions)
    B1, U, D = FindBallotChangeMulti(Lv, Lc, portions,qmax)
    B2, U, D = FindBallotChangeMulti(Lv, Lc, portions,qmin)
    B, Umax, Dmin = FindBallotChangeMulti(Lv,Lc,portions,qmax-1)
    B, Umin, Dmax = FindBallotChangeMulti(Lv,Lc,portions,qmin+1)
    B3 = 0
    q = -1
    if Dmin > Umax:
        B3 = Dmin
    elif Dmin < Umin and Dmax < Umin:
        B3 = Umin
    else:
        qleft = qmax - 1
        qright = qmin + 1
        print(qleft, qright)
        while qleft - qright > 1:
            q = (qleft + qright)/2
            Bq, Uq, Dq = FindBallotChangeMulti(Lv,Lc,portions,q)
            if Dq < Uq:
                qleft = q
            else:
                qright = q
            if qleft - qright == 1:
                Bql, Uql, Dql = FindBallotChangeMulti(Lv,Lc,portions,qleft)
                Bqr, Uqr, Dqr = FindBallotChangeMulti(Lv,Lc,portions,qright)
                B3 = min(Bql,Bqr)
    print(B1,B2,B3)
    margin = min(min(B1,B2),B3)
