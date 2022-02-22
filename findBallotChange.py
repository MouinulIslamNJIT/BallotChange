def findBallotChange(Lv,Lc,ia,ib,q,a,b,aq,bq):

    ballotChange = 0

    if(q < Lv[ia]):

        ballotChange = aq - a + bq - b

    elif (q > Lv[ib]):
        ballotChange = a - aq + b - bq

    elif(Lv[ib] < q < Lv[ia]):

        ballotChange  = (aq -a)* (q - 1) + (b - bq) * q

    return ballotChange

def findBallotChange_multigroups(Lv,Lc,I,q,Quotas,QGroups):
    ballotChange = 0
    return ballotChange