import numpy as np

def get_cost(ch1, ch2):
    if(ch1 == ch2):
        return 0
    return 1

def cer(target, pred):
    len_t = len(target)
    len_p = len(pred)
    if(len_t == 0 or len_p == 0):
        print("no string", target)
        return 0
    dis = np.zeros((len_t+1, len_p+1)) #t行p列
    for i in range(len_t + 1):
        dis[i][0] = i
    for j in range(len_p + 1):
        dis[0][j] = j
    for i in range(1, len_t + 1):
        char1 = target[i-1]
        for j in range(1, len_p + 1):
            char2 = pred[j-1]
            dis[i][j] = min( dis[i-1][j]+1, dis[i][j-1]+1, dis[i-1][j-1]+get_cost(char1, char2))
    return dis[len_t][len_p] / max(len_t, len_p)

#print( cer("abcd", "acde") )

