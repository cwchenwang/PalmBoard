import scipy.stats
import numpy as np
import pickle
import utils
# slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)


abs_pos = { 'q': [0,2], 'w': [1,2], 'e': [2,2], 'r': [3,2], 't':[4,2], 'y':[5,2], 'u':[6,2], 'i':[7,2], 'o':[8,2], 'p':[9,2], 'a':[0.25, 1], 's':[1.25,1], 'd':[2.25,1], 'f':[3.25,1], 'g':[4.25,1], 'h':[5.25,1], 'j':[6.25,1], 'k':[7.25,1], 'l':[8.25,1], 'z':[0.75, 0], 'x':[1.75,0], 'c':[2.75,0], 'v':[3.75,0], 'b':[4.75, 0], 'n'
:[5.75, 0], 'm': [6.75, 0] }

# tep_pos = { 'q': [0,4], 'w': [2,4], 'e': [4,4], 'r': [6,4], 't':[8,4], 'y':[10,4], 'u':[12,4], 'i':[14,4], 'o':[16,4], 'p':[18,4], 'a':[0.5, 2], 's':[2.5,2], 'd':[4.5,2], 'f':[6.5,2], 'g':[8.5,2], 'h':[10.5,2], 'j':[12.5,2], 'k':[14.5,2], 'l':[16.5,2], 'z':[1.5, 0], 'x':[3.5,0], 'c':[5.5,0], 'v':[7.5,0], 'b':[9.5, 0], 'n'
# :[11.5, 0], 'm': [13.5, 0] }

path="/Volumes/Seagate Exp/data/"

# x = []
# X = []
# y = []
# Y = []
# for item in tep_pos:
#     char = item
#     if(char != ' '):
#         x.append(float(tep_pos[item][0]))
#         y.append(float(tep_pos[item][1]))
#         X.append(abs_pos[char][0])
#         Y.append(abs_pos[char][1])
# slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(X, x)
# print(len(x))
# print(r_value**2)

# def abs_ind(name, mode):
#     with open("../../data/"+name+"-"+mode+"-center.csv") as f:
#         x = []
#         X = []
#         y = []
#         Y = []
#         lines = f.readlines()
#         for line in lines:
#             line = line[:-1]
#             line = line.split(",")
#             char = line[0]
#             if(char != ' ' and utils.is_right(char)):
#                 x.append(float(line[1]))
#                 y.append(float(line[2]))
#                 X.append(abs_pos[char][0])
#                 Y.append(abs_pos[char][1])
#         slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(X, x)
#         slope, intercept, r_value2, p_value, std_err = scipy.stats.linregress(Y, y)
#         # print(len(x))
#         print(str(r_value**2)+","+str(r_value2**2)+","+mode+","+name+",absolute,half")

# def abs_pooled():
#     x = []
#     X = []
#     y = []
#     Y = []
#     with open("../../data/all-norm.csv") as f:
#         f.readline()
#         lines = f.readlines()
#         for line in lines:
#             line = line[:-1]
#             line = line.split(",")
#             char = line[4]
#             if(char != 'blank'):
#                 x.append(float(line[2]))
#                 y.append(float(line[3]))
#                 X.append(abs_pos[char][0])
#                 Y.append(abs_pos[char][1])
#     slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(X, x)
#     print(len(x))
#     print(r_value**2)
#     slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(Y, y)
#     print(r_value**2)

def remove_3d_outliers(data):
    # print(len(data))
    new_data = np.empty(shape=(0,2))
    x = data[:,0]
    y = data[:,1]
    x_dev = np.std(x, axis=0)
    y_dev = np.std(y, axis=0)
    x_mean = np.sum(x)/len(x)
    y_mean = np.sum(y)/len(y)
    for item in data:
        if(x_mean-3*x_dev <= item[0] and item[0] <= x_mean+3*x_dev and y_mean-3*y_dev <= item[1] and item[1] <= y_mean+3*y_dev):
            new_data = np.append(new_data, [item], axis=0)
    # print(len(new_data))
    return new_data

def abs_ind(name, mode):
    data = pickle.load(open(path+mode+"/"+name+"/mapping.pkl", 'rb'))
    x = []
    X = []
    y = []
    Y = []
    for char in data:
        # if char != ' ' and utils.is_right(char):
        if char != " ":
            new_data = remove_3d_outliers(data[char])
            x0 = new_data[:,0]
            y0 = new_data[:,1]
            for i in range(len(x0)):
                x.append(x0[i])
                X.append(abs_pos[char][0])
                y.append(y0[i])
                Y.append(abs_pos[char][1])
        #     mx = data[char][:,0]
        #     my = data[char][:,1]
        #     mx = np.sum(mx)/len(mx)
        #     my = np.sum(my)/len(my)
        #     x.append(mx)
        #     y.append(my)
        #     X.append(abs_pos[char][0])
        #     Y.append(abs_pos[char][1])

    # print(len(x))
    slope1, intercept1, r_value1, p_value, std_err = scipy.stats.linregress(X, x)
#     print(r_value**2)
    slope2, intercept2, r_value2, p_value, std_err = scipy.stats.linregress(Y, y)
#     print(r_value**2)
    return (slope1, intercept1, r_value1, slope2, intercept2, r_value2)
# abs_pooled()

names = [ "wangchen1", "cai", "czt", "fjy", "fsq", "gsh", "lc", "luyiqin", "lwk", "lxy", "qdn", "wyd"]

x = []
X = []
y = []
Y = []
mx = 47.64
my = 151.55

def get_deviation(data):
    xf = data['f'][:, 0]
    yf = data['f'][:, 1]
    xj = data['j'][:, 0]
    yj = data['j'][:, 1]
    xf = np.sum(xf)/len(xf)
    yf = np.sum(yf)/len(yf)
    xj = np.sum(xj)/len(xj)
    yj = np.sum(yj)/len(yj)
    return (mx - xf/2 - xj/2, my-yf/2-yj/2)

for name in names:
    for mode in ["hover", "place"]:
    #     (s1, i1, r1, s2, i2, r2) = abs_ind(name, mode)
    #     print(str(s1) + "," + str(i1) + "," + str(r1)+","+str(s2) + "," + str(i2) + "," + str(r2) + "," +mode+","+name+",absolute,all,whole")
        data = pickle.load(open(path+mode+"/"+name+"/mapping.pkl", 'rb'))
        (xd, yd) = get_deviation(data)
        for char in data:
            # if char != ' ' and utils.is_right(char):
            if char != " ":
                new_data = remove_3d_outliers(data[char])
                x0 = new_data[:,0]
                y0 = new_data[:,1]
                for i in range(len(x0)):
                    x.append(x0[i]+xd)
                    X.append(abs_pos[char][0])
                    y.append(y0[i]+yd)
                    Y.append(abs_pos[char][1])
            #     mx = data[char][:,0]
            #     my = data[char][:,1]
            #     mx = np.sum(mx)/len(mx)
            #     my = np.sum(my)/len(my)
            #     x.append(mx)
            #     y.append(my)
            #     X.append(abs_pos[char][0])
            #     Y.append(abs_pos[char][1])

        # print(len(x))
slope1, intercept1, r_value1, p_value, std_err = scipy.stats.linregress(X, x)
#     print(r_value**2)
slope2, intercept2, r_value2, p_value, std_err = scipy.stats.linregress(Y, y)
    #     print(r_value**2)
print(slope1, intercept1, r_value1, slope2, intercept2, r_value2)
print(slope1*1.319, intercept1*1.319, r_value1, slope2*1.297, intercept2*1.297, r_value2)