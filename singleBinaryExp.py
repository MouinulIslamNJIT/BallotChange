import pandas as pd
from calculateMargin import *
from findBallotChange import *


bronx = pd.read_csv('Bronx Justice of the Supreme Court.csv')
bronx = bronx.sort_values(by=['Votes'],ascending = False)

Lv = list(bronx['Votes'])
Lc = list(bronx['Party'])

for i in range(len(Lc)):
    if Lc[i] == "Democratic":
        Lc[i] = "B"
    else:
        Lc[i] = "A"
portion = {'B':4,'A':1}

print(Lv)

#%%

ours = calculateMargin(Lv,Lc,1,4)
print(ours)
idxLc = []
for i in range(len(Lc)):
    if Lc[i] == "B":
        idxLc.append(1)
    else:
        idxLc.append(0)
portion = {0:1,1:4}

diversetopk = calculateMargin_selectTopK(Lv,idxLc,5,list(portion.values()))

ilpLc = [i for i in Lc]
portion = {'A':1,'B':4}
# ILP = AlgOptMFMultiMore(Lv,Lc,5,portion)
print("NYC election results(k=5):")
print("ours:",ours)
print("diverse top k:",diversetopk)
#





