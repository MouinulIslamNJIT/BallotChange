import pandas as pd
from calculateMargin import calculateMargin_multigroup
from randomInputGenerator import *
from multiAttributesBallotChange import *
##########################Australia Election###################################
data = pd.read_csv('SenateStateFirstPrefsByPollingPlaceDownload-24310-NSW.csv')
data = data.sort_values(by = ['OrdinaryVotes'], ascending = False)
australia_Lv = list(data['OrdinaryVotes'])
australia_Lc = list(data['Party'])
genredict = dict(data['Party'].value_counts())
k = 6
portions = queryGenerator(k,genredict)
Lcdict = {}
for idx,i in enumerate(portions.keys()):
    Lcdict[i] = idx
idxLc = []
idxLv = []
normal_Lc = []
for i,j in zip(australia_Lc,australia_Lv):
    if pd.isna(i)!=True:
        idxLc.append(Lcdict[i])
        normal_Lc.append(australia_Lc)
        idxLv.append(j)
print("data ready!")
####         algorithms         #####
ours = calculateMargin_multigroup(idxLv,idxLc,list(portions.values()))
diversetopk = calculateMargin_selectTopK(idxLv,idxLc,k,list(portions.values()))
ILP = AlgOptMFMultiMore(idxLv,normal_Lc,portions)


#################################################     MovieLens
ml_matrix = pd.read_csv('25m_movie100.csv',index_col=0)
maxValueIndex = ml_matrix.idxmax(axis = 1)
users = list(maxValueIndex.keys())
votes = maxValueIndex.value_counts()
movies =list(votes.keys())
items= pd.read_csv('movies.csv',index_col=0)
movieGenre = {}
movieName = {}
for index,i in items.iterrows():
    movieGenre[i['movieId']] = i['genres']
    movieName[i['movieId']] = i['title']






