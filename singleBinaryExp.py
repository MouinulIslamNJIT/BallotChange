import pandas as pd
from calculateMargin import *
from randomInputGenerator import *
import csv


bronx = pd.read_csv('Bronx Justice of the Supreme Court.csv')
bronx = bronx.sort_values(by=['Votes'],ascending = False)



Lv = list(bronx['Votes'])
Lc = list(bronx['Party'])
LcDict = {}
for i in range(len(Lc)):
    if Lc[i] == "Democratic":
        Lc[i] = "B"
        LcDict.setdefault('B', 0)
        LcDict['B'] += 1
    else:
        Lc[i] = "A"
        LcDict.setdefault('A', 0)
        LcDict['A'] += 1
kRange = [2, 4, 6]
for k in kRange:
    portion = queryGenerator(k,LcDict)

    ours = calculateMargin(Lv,Lc,portion['A'],portion['B'])
    print("k= ",k,"ours",ours)
    diversetopk = calculateMargin_selectTopK(Lv,Lc,5,portion)
    print("k= ",k,"diversetopk:",diversetopk)

# ilpLc = [i for i in Lc]
# portion = {'A':1,'B':4}
# ILP = AlgOptMFMultiMore(Lv,Lc,5,portion)

#
# k = 5
#
# with open('topkSet.csv', newline='') as f:
#     reader = csv.reader(f)
#     leximinSet = [int(i) for i in list(reader)[0]]
#
# leximin = findMarginLexi(Lv, Lc, leximinSet,k)
# # print("NYC election results(k=5):")
# # print("ours:",ours)
# # print("diverse top k:",diversetopk)
# # print("ILP:",ILP)
# print("leximin:",leximin)
#
