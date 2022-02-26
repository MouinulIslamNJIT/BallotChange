def findBallotChange(Lv, Lc, q, a, b, qmin, qmax):
    Bq = 0
    Dq = 0
    Uq = 0
    Lva = [i for (i, j) in zip(Lv, Lc) if j == "A"]
    Lvb = [i for (i, j) in zip(Lv, Lc) if j == "B"]
    aStar = {q - 1: 0, q: 0, q + 1: 0}
    bStar = {q - 1: 0, q: 0, q + 1: 0}
    for (i, j) in zip(Lv, Lc):
        if j == 'A':
            if i >= q + 1:
                aStar[q + 1] += 1
            if i >= q:
                aStar[q] += 1
            if i >= q - 1:
                aStar[q - 1] += 1
        if j == "B":
            if i >= q + 1:
                bStar[q + 1] += 1
            if i >= q:
                bStar[q] += 1
            if i >= q - 1:
                bStar[q - 1] += 1
    if q == qmin and q == qmax:
        B1a = a - aStar[q + 1] + b - bStar[q + 1]
        B1b = aStar[q] - a + bStar[q] - b
        B1c = max(a - aStar[q + 1], aStar[q] - a)
        B1d = max(b - bStar[q + 1], bStar[q] - b)
        Bq = min(min(B1a, B1b), min(B1c, B1d))
    elif q == qmax and q > qmin:
        L1_qplus1_a = [i for i in Lva if i < q + 1]
        U1_qplus1 = (q + 1) * (a - aStar[q + 1]) - sum(
            [L1_qplus1_a[i] for i in range(min(len(L1_qplus1_a), a - aStar[q + 1]))])
        L2_q_a = [i for i in Lva if i < q]
        U2_q = q * (a - aStar[q]) - sum([L2_q_a[i] for i in range(min(len(L2_q_a), a - aStar[q]))])
        L1_q_b = [i for i in Lvb if i >= q]
        L1_q_b.sort()
        Dq = sum([L1_q_b[i] for i in range(min(len(L1_q_b), bStar[q] - b))]) - ((q - 1) * (bStar[q] - b))
        Bq = min(U1_qplus1, max(U2_q, Dq))
    elif q >= qmin and q < qmax:
        L_q_a = [i for i in Lva if i < q]
        if a > aStar[q]:
            Uq = q * (a - aStar[q]) - sum([L_q_a[i] for i in range(min(len(L_q_a), a - aStar[q]))])
        else:
            Uq = 0
        L_q_b = [i for i in Lvb if i >= q]
        L_q_b.sort()
        Dq = sum([L_q_b[i] for i in range(min(len(L_q_b), bStar[q] - b))]) - ((q - 1) * (bStar[q] - b))
        Bq = max(Uq, Dq)
    return Bq, Uq, Dq


def FindBallotChangeMulti(Lv, Lc, a, q):
    attrArray = list(set(Lc))
    attrArray

    LvArray = []
    for val in attrArray:
        LvArray.append([i for (i, j) in zip(Lv, Lc) if j == val])

    Lqu = []
    Lqd = []
    Lqu_plus_one = []
    for val in attrArray:
        Lqu.append([i for i in LvArray[val] if i < q])
        Lqu_plus_one.append([i for i in LvArray[val] if i < q + 1])
        lst = [i for i in LvArray[val] if i >= q]
        lst.sort()
        Lqd.append(lst)

    aStarq = []
    for val in attrArray:
        aStarq.append(len([i for i in LvArray[val] if i >= q]))
    aStarq

    aStarq_minus_one = []
    for val in attrArray:
        aStarq_minus_one.append(len([i for i in LvArray[val] if i >= q - 1]))
    aStarq_minus_one

    aStarq_plus_one = []
    for val in attrArray:
        aStarq_plus_one.append(len([i for i in LvArray[val] if i >= q + 1]))
    aStarq_plus_one

    Uq = 0
    Dq = 0
    for val in attrArray:
        if a[val] > aStarq[val]:
            v = q * (a[val] - aStarq[val]) - sum([Lqu[val][i] for i in range(a[val] - aStarq[val])])
            Uq = Uq + v

        if a[val] <= aStarq[val]:
            v = sum([Lqd[val][i] for i in range(aStarq[val] - a[val])]) - (q - 1) * (aStarq[val] - a[val])
            Dq = Dq + v
    ballotChange = max(Dq, Uq)
    Bq = ballotChange
    print("margin at q = ", q, " is = ", ballotChange)

    Uq_ties = 0
    Dq_ties = 0
    ballotChange_ties = 1000000
    maxqval = -10
    maxdif = -10
    for val in attrArray:
        if a[val] < aStarq[val] and aStarq_plus_one[val] < a[val]:
            diff = aStarq[val] - aStarq_plus_one[val]
            if diff > maxdif:
                maxqval = val
                maxdif = diff

    if maxqval >= 0:
        for val in attrArray:
            if a[val] > aStarq[val]:
                v = (q + 1) * (a[val] - aStarq_plus_one[val]) - sum(
                    [Lqu_plus_one[val][i] for i in range(a[val] - aStarq_plus_one[val])])
                Uq_ties = Uq_ties + v

            if a[val] <= aStarq[val] and val != maxqval:
                v = sum([Lqd[val][i] for i in range(aStarq[val] - a[val])]) - (q - 1) * (aStarq[val] - a[val])
                Dq_ties = Dq_ties + v
        ballotChange_ties = max(Dq_ties, Uq_ties)

    print("margin at q = ", q, " with ties  = ", ballotChange_ties)

    if ballotChange_ties < ballotChange:
        Dq = Dq_ties
        Uq = Uq_ties
        Bq = ballotChange_ties
    return Bq, Uq, Dq
