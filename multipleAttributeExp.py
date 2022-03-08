import pandas as pd
from calculateMargin import calculateMargin_multigroup, calculateMargin_selectTopK,AlgOptMFMultiMore,AlgMFMulti2
from multiAttributesBallotChange import *
from randomInputGenerator import *
from dataWriter import dataWriter
import numpy as np
import random
np.random.seed(0)
random.seed(0)
#
#
# data = pd.read_csv('SenateStateFirstPrefsByPollingPlaceDownload-24310-NSW.csv')
# candidates = pd.read_csv('SenateCandidatesDownload-24310.csv')
# print("read finished")
#
# candiVotes = {}
# candiParty = {}
# candiHistoricElected = {}
# allCandidates = set(candidates['CandidateID'])
#
# for idx,i in candidates.iterrows():
#     candiHistoricElected[i['CandidateID']] = i['HistoricElected']
#
# for idx,i in data.iterrows():
#     if pd.isna(i['Party']) == 0 and i['CandidateID'] in allCandidates:
#         candiVotes.setdefault(i['CandidateID'],0)
#         candiVotes[i['CandidateID']] += i['OrdinaryVotes']
#         candiParty[i['CandidateID']] = i['Party']
# print("load finished")
# items = []
# for i in candiParty.keys():
#     items.append([candiVotes[i],candiParty[i],candiHistoricElected[i]])
# items.sort(reverse=True)
# australia_Lv = [i[0] for i in items]
# australia_Lc = [(i[1],i[2]) for i in items]
#
# featureData = pd.DataFrame(australia_Lc,columns=['party','HistoricElected'])
# partyDict = dict(featureData['party'].value_counts())
# historicDict = dict(featureData['HistoricElected'].value_counts())
# YDict = dict(featureData[featureData['HistoricElected'] == 'Y']['party'].value_counts())

kRange = [4,6,8,10,12]
for k in kRange:
    print("k = ",k)
    # print("ydict:", YDict)
    # historicPortion = queryGenerator(k,historicDict)
    # partyPortion = queryGenerator_party(k,partyDict,historicPortion['Y'], YDict)
    #
    # print(historicPortion)
    # # for i in partyPortion.items():
    # #     if i[1] == 1:
    # #         print(i[0])
    # portionList = [partyPortion,historicPortion]
    # dataWriter(australia_Lv,australia_Lc,portionList,"aus_multiAttribute_k="+str(k)+'_')
    # print("data finished")
    dataStr = "aus_multiAttribute_k="+str(k)+"_Data.pkl"

    ProtionStr = "aus_multiAttribute_k="+str(k)+"_Portion.pkl"
    aus_data = pd.read_pickle(dataStr)
    portion = pd.read_pickle(ProtionStr)
    # print("aus_multiAttribute_k=4_Data.pkl")
    # print(portion)
    Lv = list(aus_data["Lv"])
    Lc = list(aus_data['Lc'])
    portionParty = dict(portion.iloc[:-2].values)
    portionHistoric = dict(portion.iloc[-2:].values)
    portionList = [portionParty, portionHistoric]
    #
    print("data ready!")
    ourCross = cartesianProductMargin(Lv,Lc,k,portionList)
    print("our cross:", ourCross,"k= ",k)
    # topkCross = cartesianProductDiverseTopKIndep(Lv, Lc, k, portionList)
    # print("topk cross:", topkCross)
    indep = cartesianProductDiverseTopKIndep(Lv, Lc, k, portionList)
    print("independent topk cross:", indep,"k= ",k)
    # aprx2 = AlgMFMulti2(Lv,Lc,portionList,k)
    # print("approximation algorithm:", aprx2,"k= ",k)


# Lv = [17,14,12,11,11,10,10,9,9,5,5]
# Lc = [ ('Male', 'Junior'),
#     ('Male', 'Junior'),
#     ('Male', 'Mid'),
#     ('Male', 'Senior'),
#     ('Female', 'Junior'),
#     ('Female', 'Junior'),
#     ('Female', 'Junior'),
#     ('Female', 'Senior'),
#     ('Female', 'Senior'),
#     ('Female', 'Mid'),
#     ('Female', 'Mid')]
# a = [{'Male':2,'Female':2},{'Junior':2,'Mid':1,'Senior':1}]
#
# k = 4
#
# print(cartesianProductMargin(Lv,Lc,k,a))
#
