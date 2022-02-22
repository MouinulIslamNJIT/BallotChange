import numpy as np
def rank_generator(num_candidate:int, vote_range: list, num_group:int, group_distribution = [-1]):
    lv = list(np.random.randint(low = vote_range[0], high=vote_range[1], size = num_candidate))
    lv.sort(reverse=True)
    if group_distribution == [-1]:
        lc = list(np.random.choice(range(num_group),size = num_candidate))
    return lv,lc



