import pickle
import scipy.stats
import utils
import numpy as np


names = [ "cai", "czt", "fjy", "fsq", "gsh", "lc", "luyiqin", "lwk", "lxy", "qdn", "wyd", "wangchen1"]
abs_pos = { 'q': [0,2], 'w': [1,2], 'e': [2,2], 'r': [3,2], 't':[4,2], 'y':[5,2], 'u':[6,2], 'i':[7,2], 'o':[8,2], 'p':[9,2], 'a':[0.25, 1], 's':[1.25,1], 'd':[2.25,1], 'f':[3.25,1], 'g':[4.25,1], 'h':[5.25,1], 'j':[6.25,1], 'k':[7.25,1], 'l':[8.25,1], 'z':[0.75, 0], 'x':[1.75,0], 'c':[2.75,0], 'v':[3.75,0], 'b':[4.75, 0], 'n':[5.75, 0], 'm': [6.75, 0] }

# abs_pos = utils.abs_pos_arc

# x = []
# X = []
# y = []
# Y = []

def get_relative(path):
    counter = {}

    rel_dict = {}

    for i in range(97, 123):
        for j in range(97, 123):
            dx = int(abs_pos[chr(i)][0] - abs_pos[chr(j)][0])
            dy = int(abs_pos[chr(i)][1] - abs_pos[chr(j)][1])
            rel_dict["x"+str(dx)] = []
            rel_dict["y"+str(dy)] = []

    x = []
    X = []
    y = []
    Y = []
    for name in names:
        for mode in ["place", "hover"]:
            print(name, mode)
            for i in range(97, 123):
                counter[chr(i)] = 0
            words = []
            f = open(path+mode+"/"+name+"/sentences", 'r')

            lines = f.readlines()
            for line in lines:
                line = line[:-1]
                line = line.split(" ")
                for item in line:
                    words.append(item.lower())
                    # for char in item:
                    #     if char != " ":
                    #         counter[char.lower()] += 1
            f.close()

            data = pickle.load(open(path+mode+"/"+name+"/"+"mapping.pkl", 'rb'))
            # for item in data:
            #     if item != " ":
            #         if(len(data[item]) != counter[item]):
            #             print('ha')
            
        
            for word in words:
                for i in range(len(word)-1):
                    ch1 = word[i]
                    ch2 = word[i+1]
                    dx = int(abs_pos[ch2][0] - abs_pos[ch1][0])
                    dy = int(abs_pos[ch2][1] - abs_pos[ch1][1])
                    # print(ch1, ch2)
                    # print(data[ch1][counter[ch1]], data[ch2][counter[ch2]])

                    # if(utils.is_right(ch1) and utils.is_right(ch2)):
                    if True:
                        # print(rel_dict[ch1+ch2])
                        # print(key, ch1, counter[ch1])
                        if(ch1 == ch2):
                            # if(data[ch2][counter[ch2]+1][0] - data[ch1][counter[ch1]][0] > 10):
                            #     print(ch1, ch2, data[ch2][counter[ch2]+1][0] - data[ch1][counter[ch1]][0], data[ch2][counter[ch2]+1][1] - data[ch1][counter[ch1]][1], rel_dict["x0"])
                            rel_dict["x"+str(dx)].append(data[ch2][counter[ch2]+1][0] - data[ch1][counter[ch1]][0])

                            # print(rel_dict["x0"], data[ch2][counter[ch2]+1][0] - data[ch1][counter[ch1]][0])
                            # print(max(rel_dict["x0"]), data[ch2][counter[ch2]+1][0] - data[ch1][counter[ch1]][0])
                            rel_dict["y"+str(dy)].append(data[ch2][counter[ch2]+1][1] - data[ch1][counter[ch1]][1])
                        else:
                            rel_dict["x"+str(dx)].append(data[ch2][counter[ch2]][0] - data[ch1][counter[ch1]][0])
                            rel_dict["y"+str(dy)].append(data[ch2][counter[ch2]][1] - data[ch1][counter[ch1]][1])
                        # print(rel_dict[ch1+ch2])

                        # x.append(data[ch2][counter[ch2]][0]-data[ch1][counter[ch1]][0])
                        # X.append(abs_pos[ch2][0] - abs_pos[ch1][0])
                        # y.append(data[ch2][counter[ch2]][1]-data[ch1][counter[ch1]][1])
                        # Y.append(abs_pos[ch2][1] - abs_pos[ch1][1])

                    counter[ch1] += 1
                    # if(ch1 == "n"):
                    #     print(ch1, counter[ch1], word)
                    if(i == len(word) - 2):
                        counter[ch2] += 1

            f = open("../../data/"+name+"-"+mode+"-rela.csv", 'w')
            for pair in rel_dict:
                if(len(rel_dict[pair]) > 0):
                    # print(rel_dict[pair])
                    # if(utils.is_right(ch1) and utils.is_right(ch2)):
                    if True:
                        # mx = rel_dict[pair][:,0]
                        # my = rel_dict[pair][:,1]
                        # cx = np.sum(mx)/len(mx)
                        # cy = np.sum(my)/len(my)
                        # dx = np.std(mx, axis=0)
                        # dy = np.std(my, axis=0)
                        # f.write(pair+","+str(cx)+","+str(cy)+","+str(dx)+","+str(dy)+"\n")

                        mx = rel_dict[pair]
                        
                        cx = np.sum(mx)/len(mx)

                        dx = np.std(mx, axis=0)

                        # print(name, mode, pair, cx, cy, dx, dy)
                        f.write(pair+","+str(cx)+","+str(dx)+"\n")
                        # x.append(mx)
                        # y.append(my)
                        # X.append(abs_pos[pair[1]][0] - abs_pos[pair[0]][0])
                        # Y.append(abs_pos[pair[1]][1] - abs_pos[pair[0]][1])
            f.close()
    # f = open("../../data/all-rela.csv", 'w')
    # for pair in rel_dict:
    #     if(len(rel_dict[pair]) > 0):
    #         # print(rel_dict[pair])
    #         # if(utils.is_right(ch1) and utils.is_right(ch2)):
    #         if True:
    #             # mx = rel_dict[pair][:,0]
    #             # my = rel_dict[pair][:,1]
    #             # cx = np.sum(mx)/len(mx)
    #             # cy = np.sum(my)/len(my)
    #             # dx = np.std(mx, axis=0)
    #             # dy = np.std(my, axis=0)
    #             # f.write(pair+","+str(cx)+","+str(cy)+","+str(dx)+","+str(dy)+"\n")

    #             mx = rel_dict[pair]
                
    #             cx = np.sum(mx)/len(mx)

    #             dx = np.std(mx, axis=0)

    #             # print(name, mode, pair, cx, cy, dx, dy)
    #             f.write(pair+","+str(cx)+","+str(dx)+"\n")
    #             # x.append(mx)
    #             # y.append(my)
    #             # X.append(abs_pos[pair[1]][0] - abs_pos[pair[0]][0])
    #             # Y.append(abs_pos[pair[1]][1] - abs_pos[pair[0]][1])
    # f.close()

def get_mean_relative(path, name, mode):
    counter = {}

    rel_dict = {}

    for i in range(97, 123):
        for j in range(97, 123):
            rel_dict[chr(i)+chr(j)] = np.empty(shape=(0,2))

    for i in range(97, 123):
        counter[chr(i)] = 0

    words = []
    f = open(path+"sentences", 'r')
    lines = f.readlines()
    for line in lines:
        line = line[:-1]
        line = line.split(" ")
        for item in line:
            words.append(item.lower())
            # for char in item:
            #     if char != " ":
            #         counter[char.lower()] += 1
    f.close()
    # print(counter)
    data = pickle.load(open(path+"mapping.pkl", 'rb'))
    # for item in data:
    #     if item != " ":
    #         if(len(data[item]) != counter[item]):
    #             print(item, len(data[item], counter, path))
    
    # rel_dict = {}
    x = []
    X = []
    y = []
    Y = []

    for word in words:
        for i in range(len(word)-1):
            ch1 = word[i]
            ch2 = word[i+1]
            # print(ch1, ch2)
            # print(data[ch1][counter[ch1]], data[ch2][counter[ch2]])

            # if(utils.is_right(ch1) and utils.is_right(ch2)):
            if True:
                # print(rel_dict[ch1+ch2])
                rel_dict[ch1+ch2] = np.append(rel_dict[ch1+ch2], [[ data[ch2][counter[ch2]][0]-data[ch1][counter[ch1]][0], data[ch2][counter[ch2]][1]- data[ch1][counter[ch1]][1] ]], axis=0)
                # print(rel_dict[ch1+ch2])

                # x.append(data[ch2][counter[ch2]][0]-data[ch1][counter[ch1]][0])
                # X.append(abs_pos[ch2][0] - abs_pos[ch1][0])
                # y.append(data[ch2][counter[ch2]][1]-data[ch1][counter[ch1]][1])
                # Y.append(abs_pos[ch2][1] - abs_pos[ch1][1])

            counter[ch1] += 1
            if(i == len(word) - 2):
                counter[ch2] += 1
    # print(rel_dict)
    f = open("../../data/"+name+"-"+mode+"-rela.csv", 'w')
    for pair in rel_dict:
        if(len(rel_dict[pair]) > 0):
            # print(rel_dict[pair])
            # if(utils.is_right(ch1) and utils.is_right(ch2)):
            if True:
                mx = rel_dict[pair][:,0]
                my = rel_dict[pair][:,1]
                cx = np.sum(mx)/len(mx)
                cy = np.sum(my)/len(my)
                dx = np.std(mx, axis=0)
                dy = np.std(my, axis=0)
                # print(name, mode, pair, cx, cy, dx, dy)
                f.write(pair+","+str(cx)+","+str(cy)+","+str(dx)+","+str(dy)+"\n")
                # x.append(mx)
                # y.append(my)
                # X.append(abs_pos[pair[1]][0] - abs_pos[pair[0]][0])
                # Y.append(abs_pos[pair[1]][1] - abs_pos[pair[0]][1])
    f.close()

    # slope1, intercept1, r_value1, p_value, std_err = scipy.stats.linregress(X, x)
    # # print(r_value**2)
    # slope2, intercept2, r_value2, p_value, std_err = scipy.stats.linregress(Y, y)
    # # print(r_value**2)
    # return (slope1, intercept1, r_value1**2, slope2, intercept2, r_value2**2)

# 一个人的 path是对应文件夹的path
def get_personal_relative(path):
    counter = {}
    for i in range(97, 123):
        counter[chr(i)] = 0
    words = []
    f = open(path+"sentences", 'r')
    lines = f.readlines()
    for line in lines:
        line = line[:-1]
        line = line.split(" ")
        for item in line:
            words.append(item.lower())
            # for char in item:
            #     if char != " ":
            #         counter[char.lower()] += 1
    f.close()
    # print(counter)
    data = pickle.load(open(path+"mapping.pkl", 'rb'))
    # for item in data:
    #     if item != " ":
    #         if(len(data[item]) != counter[item]):
    #             print(item, len(data[item], counter, path))
    
    # rel_dict = {}
    x = []
    X = []
    y = []
    Y = []
    for word in words:
        for i in range(len(word)-1):
            ch1 = word[i]
            ch2 = word[i+1]
            # print(ch1, ch2)
            # print(data[ch1][counter[ch1]], data[ch2][counter[ch2]])

            # if(utils.is_right(ch1) and utils.is_right(ch2)):
            if True:
                x.append(data[ch2][counter[ch2]][0]-data[ch1][counter[ch1]][0])
                X.append(abs_pos[ch2][0] - abs_pos[ch1][0])
                y.append(data[ch2][counter[ch2]][1]-data[ch1][counter[ch1]][1])
                Y.append(abs_pos[ch2][1] - abs_pos[ch1][1])

            counter[ch1] += 1
            if(i == len(word) - 2):
                counter[ch2] += 1
    slope1, intercept1, r_value1, p_value, std_err = scipy.stats.linregress(X, x)
    # print(r_value**2)
    slope2, intercept2, r_value2, p_value, std_err = scipy.stats.linregress(Y, y)
    # print(r_value**2)
    return (slope1, intercept1, r_value1**2, slope2, intercept2, r_value2**2)
    
# def rel_ind_mean(path):
#     data = pickle.load(open(path+"mapping.pkl", 'rb'))
#     x = []
#     X = []
#     y = []
#     Y = []
#     mean_dict = {}

#     for char in data:
#         if char != ' ':
#             mx = data[char][:,0]
#             my = data[char][:,1]
#             mx = np.sum(mx)/len(mx)
#             my = np.sum(my)/len(my)
#             mean_dict[char] = [mx, my]

#     for i in range(97, 123):
#         for j in range(97, 123):
#             ch1 = chr(i)
#             ch2 = chr(j)
#             if(utils.is_right(ch1) and utils.is_right(ch2)):
#                 x.append(mean_dict[ch2][0] - mean_dict[ch1][0])
#                 X.append(abs_pos[ch2][0] - abs_pos[ch1][0])
#                 y.append(mean_dict[ch2][1] - mean_dict[ch1][1])
#                 Y.append(abs_pos[ch2][1] - abs_pos[ch1][1])
#     # print(len(x))
#     slope1, intercept1, r_value1, p_value, std_err = scipy.stats.linregress(X, x)
# #     print(r_value**2)
#     slope2, intercept2, r_value2, p_value, std_err = scipy.stats.linregress(Y, y)
# #     print(r_value**2)
#     return (slope1, intercept1, r_value1, slope2, intercept2, r_value2)

# x = []
# X = []
# y = []
# Y = []
# path = "/Volumes/Seagate Exp/data/"
# for name in names:
#     for mode in ["hover", "place"]:
#         path = "/Volumes/Seagate Exp/data/"+mode+"/"+name+"/"
#         counter = {}
#         for i in range(97, 123):
#             counter[chr(i)] = 0
#         words = []
#         f = open(path+"sentences", 'r')
#         lines = f.readlines()
#         for line in lines:
#             line = line[:-1]
#             line = line.split(" ")
#             for item in line:
#                 words.append(item.lower())
#                 # for char in item:
#                 #     if char != " ":
#                 #         counter[char.lower()] += 1
#         f.close()
#         # print(counter)
#         data = pickle.load(open(path+"mapping.pkl", 'rb'))
#         # for item in data:
#         #     if item != " ":
#         #         if(len(data[item]) != counter[item]):
#         #             print(item, len(data[item], counter, path))
        
#         # rel_dict = {}
#         for word in words:
#             for i in range(len(word)-1):
#                 ch1 = word[i]
#                 ch2 = word[i+1]
#                 # print(ch1, ch2)
#                 # print(data[ch1][counter[ch1]], data[ch2][counter[ch2]])

#                 # if(utils.is_right(ch1) and utils.is_right(ch2)):
#                 if True:
#                     x.append(data[ch2][counter[ch2]][0]-data[ch1][counter[ch1]][0])
#                     X.append(abs_pos[ch2][0] - abs_pos[ch1][0])
#                     y.append(data[ch2][counter[ch2]][1]-data[ch1][counter[ch1]][1])
#                     Y.append(abs_pos[ch2][1] - abs_pos[ch1][1])

#                 counter[ch1] += 1
#                 if(i == len(word) - 2):
#                     counter[ch2] += 1
# slope1, intercept1, r_value1, p_value, std_err = scipy.stats.linregress(X, x)
# print(slope1*1.319, intercept1*1.319, r_value1**2)
# slope2, intercept2, r_value2, p_value, std_err = scipy.stats.linregress(Y, y)
# print(slope2*1.297, intercept2*1.297, r_value2**2)

get_relative("/Volumes/Seagate Exp/data/")
# for name in names:
#     for mode in ["hover", "place"]:
#         get_mean_relative("/Volumes/Seagate Exp/data/"+mode+"/"+name+"/")
        # (s1, i1, r1, s2, i2, r2) = get_mean_relative("/Users/clarencewang/Desktop/sensel-typing/Debug/data/"+mode+"/"+name+"/")
        # print(str(s1) + "," + str(i1) + "," + str(r1)+","+str(s2) + "," + str(i2) + "," + str(r2) + "," +mode+","+name+",relative,whole,mean")
        # (s1, i1, r1, s2, i2, r2) = get_personal_relative("/Users/clarencewang/Desktop/sensel-typing/Debug/data/"+mode+"/"+name+"/")
        # print(str(s1) + "," + str(i1) + "," + str(r1)+","+str(s2) + "," + str(i2) + "," + str(r2) + "," +mode+","+name+",relative,whole,all")

# slope, intercept, r_value1, p_value, std_err = scipy.stats.linregress(X, x)
# slope, intercept, r_value2, p_value, std_err = scipy.stats.linregress(Y, y)
# print(r_value1**2, r_value2**2)
