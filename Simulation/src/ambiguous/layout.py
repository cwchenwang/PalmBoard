import math
import sys


default_layout = {
    0: {0:'q', 1:'w', 2:'e', 3:'r', 4:'t', 5:'y', 6:'u', 7:'i', 8:'o', 9:'p'},
    1: {0:'a', 1:'s', 2:'d', 3:'f', 4:'g', 5:'h', 6:'j', 7:'k', 8:'l'},
    2: {0:'z', 1:'x', 2:'c', 3:'v', 4:'b', 5:'n', 6:'m'}
}

def dfs(left, right, num):
    '''
    num: 得到的区间数目
    '''
    # print(left, right, num)
    if(num == 1):
        res = []
        res.append(right)
        return [ [ right ] ]
    result = []
    for i in range(left, right-num+2):
        res = dfs(i+1, right, num-1)
        # print(i, res)
        for k in range(len(res)):
            res[k].append(i)
            result.append(res[k])
    return result


def get_layout(m, n, l):
    '''
    m行n列
    得到每个字母对应的位置，以及某个位置有什么字母
    '''
    grid_layout = {}
    key_pos = {}
    for i in range(97, 123):
        key_pos[chr(i)] = [-1, -1]
    for i in range(m):
        grid_layout[i] = {}
        for j in range(n):
            grid_layout[i][j] = []
    if(m == 3):
        for k in range(m):
            for i in range(n):
                if(i != n-1):
                    left = l[k*n+i+1]
                else:
                    left = -1
                right = l[k*n+i]
                # print(left, right)
                for j in range(left+1, right+1):
                    grid_layout[k][n-i-1].append(default_layout[k][j])
                    # print(grid_layout[k][n-i-1])
                    key_pos[default_layout[k][j]] = (k, n-i-1)
    print(grid_layout)
    print(key_pos)
    return grid_layout, key_pos     
    # for i in range
    # line 0

def get_words(grid_layout, key_pos, word):
    if(len(word) == 0):
        return [""]
    char = word[0]
    all_char = grid_layout[key_pos[char][0]][key_pos[char][1]]
    res = get_words(grid_layout, key_pos, word[1:])
    result = []
    for item in all_char:
        for item2 in res:
            a = item + item2
            result.append(a)
    return result


def get_all_words(grid_layout, key_pos, all_words, word_dict):
    word_num = len(all_words)
    appeared = 0
    all = 0
    for word in all_words:
        all += 1
        cand = get_words(grid_layout, key_pos, word)
        max_prob1 = -sys.float_info.max
        max_prob2 = -sys.float_info.max
        max_prob3 = -sys.float_info.max
        # print(10000 > sys.float_info.min)
        max_word1 = max_word2 = max_word3 = ""
        # print(word, cand)
        for item in cand:
            if(word_dict.__contains__(item)):
                prob = word_dict[item]
                if(prob > max_prob1):
                    # print("hello")
                    max_prob3 = max_prob2
                    max_word3 = max_word2
                    max_prob2 = max_prob1
                    max_word2 = max_word1
                    max_prob1 = prob
                    max_word1 = item
                elif(prob > max_prob2):
                    max_prob3 = max_prob2
                    max_word3 = max_word2
                    max_prob2 = prob
                    max_word2 = item
                elif(prob > max_prob3):
                    max_prob3 = prob
                    max_word3 = item
        if(max_word1 == word or max_word2 == word or max_word3 == word):
            appeared += 1
        if(all % 100 == 0):
            print(appeared, all, word, max_word1)
        # print(appeared, max_word1, max_word2, max_word3)
    # print(appeared/word_num)
            
    # with open("../../data/words.csv", 'r') as f:
    #         lines = f.readlines()
    #         for line in lines:
    #             line = line[:-1]
    #             line = line.split(",")
    #             word_dict[len(line[0])][line[0]] = math.log( float(line[1]) )
    #             all_words.append(line[0])
    # for word in all_words:
    #     for char in word:

word_dict = {}
all_words = []
with open("../../data/words.csv", 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line[:-1]
        line = line.split(",")
        word_dict[line[0]] = math.log( float(line[1]) )
        all_words.append(line[0])
# res1 = dfs(0, 9, 3)
# res2 = dfs(0, 8, 3)
# res3 = dfs(0, 6, 3)
# print(res1, res2)
# new = []
# for item in res1:
#     for item2 in res2:
#         a = []
#         a.extend(item)
#         a.extend(item2)
#         new.append(a)
# # print(new)
# all = []
# for item in new:
#     for item2 in res3:
#         a = []
#         a.extend(item)
#         a.extend(item2)
#         all.append(a)
# print(len(all))
(grid_layout, key_pos) = get_layout(3,3,[9,5,3,8,4,2,6,4,2])

# print(get_words(grid_layout, key_pos, "hello"))

# print(get_words(grid_layout, key_pos, "something"))
get_all_words(grid_layout, key_pos, all_words, word_dict)
# print(all)
# print(res1)
# for i in range(len(res)):


