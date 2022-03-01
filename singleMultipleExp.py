import pandas as pd
from calculateMargin import calculateMargin_multigroup, calculateMargin_selectTopK,AlgOptMFMultiMore
from randomInputGenerator import *
from multiAttributesBallotChange import *
##########################Australia Election###################################
# data = pd.read_csv('SenateStateFirstPrefsByPollingPlaceDownload-24310-NSW.csv')
# data = data.sort_values(by = ['OrdinaryVotes'], ascending = False)
# australia_Lv = list(data['OrdinaryVotes'])
# australia_Lc = list(data['Party'])
# genredict = dict(data['Party'].value_counts())
# k = 6
# portions = queryGenerator(k,genredict)
# Lcdict = {}
# for idx,i in enumerate(portions.keys()):
#     Lcdict[i] = idx
# idxLc = []
# idxLv = []
# normal_Lc = []
# for i,j in zip(australia_Lc,australia_Lv):
#     if pd.isna(i)!=True:
#         idxLc.append(Lcdict[i])
#         normal_Lc.append(i)
#         idxLv.append(j)
# print("data ready!")
# ####         algorithms         #####
# ours = calculateMargin_multigroup(idxLv,idxLc,list(portions.values()))
# print("ours ready!")
# diversetopk = calculateMargin_selectTopK(idxLv,idxLc,k,list(portions.values()))
# print("diverse topk ready!")
# print("australia election results(k=6):")
# print("ours:",ours)
# print("diverse top k:",diversetopk)
# ILP = AlgOptMFMultiMore(idxLv,normal_Lc,k,portions)
# print("ILP:",ILP)

#################################################     MovieLens
ml_matrix = pd.read_csv('5star_movie_votes_9620.csv',index_col=0)

movielens_Lv = list(ml_matrix['votes'])
movies = list(ml_matrix['movieId'])
movielens_Lc = list(ml_matrix['genres'])

k = 10
groupdict = dict(ml_matrix['genres'].value_counts())
portions = queryGenerator(k,groupdict)

Lcdict = {}
for idx,i in enumerate(portions.keys()):
    Lcdict[i] = idx
idxLc = []
idxLv = []
normal_Lc = []
for i,j in zip(movielens_Lc,movielens_Lv):
    if pd.isna(i)!=True:
        idxLc.append(Lcdict[i])
        normal_Lc.append(i)
        idxLv.append(j)

#
ours = calculateMargin_multigroup(idxLv,idxLc,list(portions.values()))
diversetopk = calculateMargin_selectTopK(idxLv,idxLc,k,list(portions.values()))
# ILP = AlgOptMFMultiMore(idxLv,normal_Lc,k,portions)
print("movie lens results(k=0):")
print("ours:",ours)
print("diverse top k:",diversetopk)
# print("ILP:",ILP)
#
#





