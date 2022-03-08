import pandas as pd
from calculateMargin import calculateMargin_multigroup, calculateMargin_selectTopK,AlgOptMFMultiMore,findMarginLexi
from randomInputGenerator import *
from multiAttributesBallotChange import *
import random
import csv


np.random.seed(0)
##########################Australia Election###################################
data = pd.read_csv('SenateStateFirstPrefsByPollingPlaceDownload-24310-NSW.csv')
candiVotes = {}
candiParty = {}
for idx,i in data.iterrows():
    if pd.isna(i['Party']) == 0:
        candiVotes.setdefault(i['CandidateID'],0)
        candiVotes[i['CandidateID']] += i['OrdinaryVotes']
        candiParty[i['CandidateID']] = i['Party']
items = []
for i in candiParty.keys():
    items.append([candiVotes[i],candiParty[i]])
items.sort(reverse=True)
australia_Lv = [i[0] for i in items]
australia_Lc = [i[1] for i in items]


genredict = dict(pd.DataFrame(australia_Lc)[0].value_counts())


kRange = [4,6,8,10,12]

for k in kRange:
    portions = queryGenerator(k,genredict)
    Lcdict = {}
    for idx,i in enumerate(portions.keys()):
        Lcdict[i] = idx
    idxLc = []
    idxLv = []
    normal_Lc = []
    for i,j in zip(australia_Lc,australia_Lv):
        idxLc.append(Lcdict[i])
        normal_Lc.append(i)
        idxLv.append(j)
    print("data ready!")
    ####         algorithms         #####
    aus_ours = calculateMargin_multigroup(idxLv,normal_Lc,portions)
    print("ours ready!")
    aus_diversetopk = calculateMargin_selectTopK(idxLv,normal_Lc,k,portions)
    # aus_ILP = AlgOptMFMultiMore(idxLv,normal_Lc,k,portions)


    print("australia election results k = ",k)
    print("ours:",aus_ours)
    print("diverse top k:",aus_diversetopk)
# print("ILP:",aus_ILP)
#
# with open('leximinTopkSet.csv', newline='') as f:
#     reader = csv.reader(f)
#     leximinSet = [int(i) for i in list(reader)[0]]
#
# leximin = findMarginLexi(idxLv, idxLc, leximinSet,k)
# for i,j in portions:
#     print(i,j)
#

# print("leximin:",leximin)

#
# #################################################     MovieLens
# ml_matrix = pd.read_csv('5star_movie_votes_9620.csv',index_col=0)
# ml_matrix = ml_matrix.sort_values(by = 'votes',ascending = False)
# ml_matrix = ml_matrix.iloc[:100]
# movielens_Lv = list(ml_matrix['votes'])
# movies = list(ml_matrix['movieId'])
# movielens_Lc = list(ml_matrix['genres'])
#
# k = 10
# groupdict = dict(ml_matrix['genres'].value_counts())
# portions = queryGenerator(k,groupdict)
#
# Lcdict = {}
# for idx,i in enumerate(portions.keys()):
#     Lcdict[i] = idx
# idxLc = []
# idxLv = []
# normal_Lc = []
# for i,j in zip(movielens_Lc,movielens_Lv):
#     if pd.isna(i)!=True:
#         idxLc.append(Lcdict[i])
#         normal_Lc.append(i)
#         idxLv.append(j)
#
# #
# ours = calculateMargin_multigroup(idxLv,idxLc,list(portions.values()))
# diversetopk = calculateMargin_selectTopK(idxLv,idxLc,k,list(portions.values()))
# ILP = AlgOptMFMultiMore(idxLv,normal_Lc,k,portions)
#
#
#
# print("australia election results(k=6):")
# print("ours:",aus_ours)
# print("diverse top k:",aus_diversetopk)
# print("ILP:",aus_ILP)
#
#
#
# print("movie lens results(k=0):")
# print("ours:",ours)
# print("diverse top k:",diversetopk)
# print("ILP:",ILP)
# #
# #
# #
#
#
#
#
#
