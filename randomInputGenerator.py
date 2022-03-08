import numpy as np

np.random.seed(0)
def rankGenerator_single(num_candidate:int, vote_range: list, num_group:int, group_distribution = [-1]):
    lv = list(np.random.randint(low = vote_range[0], high=vote_range[1], size = num_candidate))
    lv.sort(reverse=True)
    if group_distribution == [-1]:
        lc = list(np.random.choice(range(num_group),size = num_candidate))
    return lv,lc

def rankGenerator_multi(num_candidate:int, vote_range: list, num_group:int, num_attri:int ,group_distribution = [-1]):
    lv = list(np.random.randint(low = vote_range[0], high=vote_range[1], size = num_candidate))
    lv.sort(reverse=True)
    lc = []
    for i in range(num_attri):
        if group_distribution == [-1]:
            attri = list(np.random.choice(range(num_group),size = num_candidate))
        lc.append(attri)
    return lv,lc


def queryGenerator(k: int, attributes: dict):
    portions = dict.fromkeys(attributes.keys(),0)
    group_set = set(attributes.keys())
    for i in range(k):
        grouplist = list(group_set)
        item = np.random.choice(grouplist)
        portions[item] += 1
        if portions[item] == attributes[item]:
            group_set.remove(item)
    return portions

def queryGenerator_party(k: int, attributes: dict,numY:int,Yattributes: dict):
    nk = k - numY
    portions = dict.fromkeys(attributes.keys(),0)
    group_set = set(attributes.keys())
    for i in range(nk):
        grouplist = list(group_set)
        item = np.random.choice(grouplist)
        portions[item] += 1
        if portions[item] == attributes[item]:
            group_set.remove(item)
    group_set = set(Yattributes.keys())
    for i in range(numY):
        grouplist = list(group_set)
        item = np.random.choice(grouplist)
        portions[item] += 1
        if Yattributes[item] == attributes[item]:
            group_set.remove(item)
    return portions
