def findBallotChange(Lv,Lc,ia,ib,q,a,b,aq,bq,qmin,qmax):
    Bq = 0
    Dq = 0
    Uq = 0
    Lva = [ i for (i,j) in zip(Lv,Lc) if i>=q and j == "A"]
    Lvb = [i for (i, j) in zip(Lv, Lc) if i >= q and j == "B"]
    aStar = {q - 1: 0, q : 0, q + 1: 0}
    bStar = {q - 1: 0, q : 0, q + 1: 0}
    for (i, j) in zip(Lv, Lc):
        if j == "A":
            if i >= q+1:
                aStar[q+1] += 1
            if i >= q:
                aStar[q] += 1
            if i >= q-1:
                aStar[q-1] += 1
        if j == "B":
            if i >= q + 1:
                bStar[q + 1] += 1
            if i >= q:
                bStar[q] += 1
            if i >= q - 1:
                bStar[q - 1] += 1
        if q == qmin and q == qmax:
            B1a = a - aStar[q+1] + b - bStar[q+1]
            B1b = aStar[q] - a + bStar[q] - b
            B1c = max(a - aStar[q+1],aStar[q] - a)
            B1d = max(b - bStar[q + 1], bStar[q] - b)
            Bq = min(min(B1a,B1b),min(B1c,B1d))
        elif q == qmax and q>qmin:
            L1_qplus1_a = [i for i in Lva if i<q+1]
            U1_qplus1 = (q+1)*(a - aStar[q+1]) - sum([L1_qplus1_a[i] for i in range(a - aStar[q+1]+1)])
            L2_q_a = [i for i in Lva if i<q]
            U2_q = q * (a - aStar[q]) - sum([L2_q_a[i] for i in range(a - aStar[q]+1)])
            L1_q_b = [i for i in Lvb if i>=q].sort()
            Dq = sum([L1_q_b[i] for i in range(bStar[q]-b+1)])
            Bq = min(U1_qplus1,max(U2_q,Dq))
        elif q >= qmin and q<qmax:
            L_q_a = [i for i in Lva if i<q]
            if a > aStar[q]:
                Uq = q * (a - aStar[q]) - sum([L_q_a[i] for i in range(a - aStar[q]+1)])
            else:
                Uq = 0
            L_q_b = [i for i in Lvb if i>=q].sort()
            Dq = sum([L_q_b[i] for i in range(bStar[q] - b + 1)]) - (q-1) * (bStar[q] - b)
            Bq = max(Uq,Dq)
    return Bq,Uq,Dq

def findBallotChange_multigroups(Lv,Lc,I,q,Quotas,QGroups):
    ballotChange = 0
    return ballotChange