import numpy as np
def diverse_top_k(I:list[list], K:int, d:list, quotas:dict) -> list:    #     I contains the all items with their category value;
    L =[]
    C = dict.fromkeys(d,0)
    slack = K - sum([np.floor(i) for i in quotas.values()])
    iter = 0
    while(len(L)<K):
        x = I[iter]
        iter += 1
        i = x[1]
        if C[i] < np.floor(quotas[i]):
            L.append(x)
            C[i] += 1
        elif(C[i]<np.ceil(quotas[i]) and slack>0):
            L.append(x)
            C[i] += 1
            slack -= 1
    return L




