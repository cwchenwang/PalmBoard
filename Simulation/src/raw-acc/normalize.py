import numpy as np 
import pickle
import os

path = "/Volumes/Seagate Exp/data/"
names = ["wangchen1", "cai", "luyiqin", "fjy", "lc",  "lwk", "lxy", "qdn", "wyd", 'czt', "gsh", "fsq"]

mode = "place"
data = pickle.load(open(path+mode+"/wangchen1"+"/"+"mapping.pkl", 'rb'))

xf = data['f'][:, 0]
yf = data['f'][:, 1]
xj = data['j'][:, 0]
yj = data['j'][:, 1]
print(xf, xj, yf, yj)
xf = np.sum(xf)/len(xf)
yf = np.sum(yf)/len(yf)
xj = np.sum(xj)/len(xj)
yj = np.sum(yj)/len(yj)
print(xf/2+xj/2, yf/2+yj/2)
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

def get_personal_offset(mode):
    dirs = os.listdir(path+mode+"/")
    f = open("offset-"+mode+".csv", 'w')
    f.write("subject, mode, dx, dy\n")
    for item in dirs:
        if os.path.isdir(path+mode+"/"+item):
            data = pickle.load(open(path+mode+"/"+item+"/"+"mapping.pkl", 'rb'))
            (xd, yd) = get_deviation(data)
            f.write(item+","+mode+","+str(xd)+","+str(yd)+"\n")
    f.close()

def cal_outliers(mode):
    dirs = os.listdir(path+mode+"/")
    tot = 0
    all = 0
    for item in names:
        if os.path.isdir(path+mode+"/"+item):
            data = pickle.load(open(path+mode+"/"+item+"/"+"mapping.pkl", 'rb'))
            (xd, yd) = get_deviation(data)
            for char in data:
                # x = data[char][:, 0]
                # y = data[char][:, 1]
                tep_data = remove_3d_outliers(data[char])
                tot += len(data[char]) - len(tep_data)
                all += len(data[char])
    print(tot, all, tot/all, mode)

def get_points(mode):
    dirs = os.listdir(path+mode+"/")
    f = open("../../data/all-norm-rm"+mode+".csv", 'w')
    f.write("subject, mode, x, y, char\n")
    for item in dirs:
        if os.path.isdir(path+mode+"/"+item):
            per_dict = {}
            for i in range(97, 123):
                per_dict[chr(i)] = np.empty(shape=(0,2))
            per_dict[' '] = np.empty(shape=(0,2)) 
            data = pickle.load(open(path+mode+"/"+item+"/"+"mapping.pkl", 'rb'))
            (xd, yd) = get_deviation(data)
            for char in data:
                # x = data[char][:, 0]
                # y = data[char][:, 1]
                tep_data = remove_3d_outliers(data[char])
                # print(len(tep_data))
                x = tep_data[:,0]
                y = tep_data[:,1]
                for i in range(len(x)):
                    per_dict[char] = np.append(per_dict[char], [[float(x[i]), float(y[i])]], axis=0)
                    if(char == ' '):
                        # print(x[i], y[i], "black")
                        f.write(item+","+mode+","+str(x[i]+xd)+"," +str(y[i]+yd)+","+str("blank")+"\n")
                    else:
                        # print(x[i], y[i], "black")
                        f.write(item+","+mode+","+str(x[i]+xd)+"," +str(y[i]+yd)+","+str(char)+"\n")
            # mx = 0
            # my = 0
            # for char in per_dict:
            #     if(char != ' '):
            #         x = per_dict[char][:,0]
            #         y = per_dict[char][:,1]
            #         # print(mode+","+item+","+char+","+str(np.std(x, axis=0)*1.319)+","+str(np.std(y, axis=0)*1.297))
            #         mx += np.std(x, axis=0)*1.319
            #         my += np.std(y, axis=0)*1.297
            # print(item+","+mode+","+str(mx/26)+","+str(my/26))
    f.close()

    all_dict = {}
    for i in range(97, 123):
        all_dict[chr(i)] = np.empty(shape=(0,2))
    all_dict['blank'] = np.empty(shape=(0,2)) 
    with open("../../data/all-norm-rm"+mode+".csv") as f:
        f.readline()
        lines = f.readlines()
        for line in lines:
            line = line[:-1]
            line = line.split(",")
            all_dict[line[4]] = np.append(all_dict[line[4]], [[float(line[2]), float(line[3])]], axis=0)

    # print(all_dict)

    f = open("../../data/all-center-"+mode+".csv", 'w')
    for char in all_dict:
        x = all_dict[char][:,0]
        y = all_dict[char][:,1]
        # x = np.sum(x) / len(x)
        # y = np.sum(y) / len(y)
        # color = np.random.rand(3,)
        # print(color)
        cx = np.sum(x) / len(x)
        cy = np.sum(y) / len(y)
        dx = np.std(x, axis=0)
        dy = np.std(y, axis=0)
        # print(char, cx, cy, dx, dy)
        # f.write(char+","+str(cx*1.319)+","+str(cy*1.297)+","+str(dx*1.319)+","+str(dy*1.297)+"\n")
        f.write(char+","+str(cx)+","+str(cy)+","+str(dx)+","+str(dy)+"\n")
    f.close()

def get_personal_points(mode):
    dirs = os.listdir(path+mode+"/")
    # f = open("../../data/all-norm-rm"+mode+".csv", 'w')
    for item in names:
        if os.path.isdir(path+mode+"/"+item):
            data = pickle.load(open(path+mode+"/"+item+"/"+"mapping.pkl", 'rb'))
            f = open("../../data/"+item+"-"+mode+"-points-norm.csv", 'w')
            f.write("subject, mode, x, y, char\n")
            (xd, yd) = get_deviation(data)
            for char in data:
                # x = data[char][:, 0]
                # y = data[char][:, 1]
                tep_data = remove_3d_outliers(data[char])
                print(len(tep_data))
                x = tep_data[:,0]
                y = tep_data[:,1]
                for i in range(len(x)):
                    if(char == ' '):
                        # print(x[i], y[i], "black")
                        f.write(item+","+mode+","+str(x[i]+xd)+"," +str(y[i]+yd)+","+str("blank")+"\n")
                    else:
                        # print(x[i], y[i], "black")
                        f.write(item+","+mode+","+str(x[i]+xd)+"," +str(y[i]+yd)+","+str(char)+"\n")
            f.close()
    all_dict = {}
    for i in range(97, 123):
        all_dict[chr(i)] = np.empty(shape=(0,2))
    all_dict['blank'] = np.empty(shape=(0,2)) 
    with open("../../data/all-norm-"+mode+".csv") as f:
        f.readline()
        lines = f.readlines()
        for line in lines:
            line = line[:-1]
            line = line.split(",")
            all_dict[line[4]] = np.append(all_dict[line[4]], [[float(line[2]), float(line[3])]], axis=0)
    print(all_dict)

    #计算每个字符的均值和标准差
    # f = open("../../data/all-center-"+mode+".csv", 'w')
    for char in all_dict:
        x = all_dict[char][:,0]
        y = all_dict[char][:,1]
        # x = np.sum(x) / len(x)
        # y = np.sum(y) / len(y)
        # color = np.random.rand(3,)
        # print(color)
        cx = np.sum(x) / len(x)
        cy = np.sum(y) / len(y)
        dx = np.std(x, axis=0)
        dy = np.std(y, axis=0)
        print(char, cx, cy, dx, dy)
        # f.write(char+","+str(cx)+","+str(cy)+","+str(dx)+","+str(dy)+"\n")
    # f.close()

def get_personal_centroids(mode):
    dirs = os.listdir(path+mode+"/")
    # f = open("../../data/all-norm-"+mode+".csv", 'w')
    # f.write("subject, mode, x, y, char\n")
    for item in dirs:
        if os.path.isdir(path+mode+"/"+item):
            print(item)
            data = pickle.load(open(path+mode+"/"+item+"/"+"mapping.pkl", 'rb'))
            f = open("../../data/"+item+"-"+mode+"-center-mm.csv", 'w')
            for char in data:
                x = data[char][:, 0]
                y = data[char][:, 1]
                cx = np.sum(x) / len(x)
                cy = np.sum(y) / len(y)
                dx = np.std(x, axis=0)
                dy = np.std(y, axis=0)
                print(char, cx, cy, dx, dy)
                f.write(char+","+str(cx*1.319)+","+str(cy*1.297)+","+str(dx*1.319)+","+str(dy*1.297)+"\n")
            f.close()
                # for i in range(len(x)):
                #     if(char == ' '):
                #         # print(x[i], y[i], "black")
                #         f.write(item+","+mode+","+str(x[i])+"," +str(y[i])+","+str("blank")+"\n")
                #     else:
                #         # print(x[i], y[i], "black")
                #         f.write(item+","+mode+","+str(x[i]+xd)+"," +str(y[i]+yd)+","+str(char)+"\n")

# cal_outliers("place")
# cal_outliers("hover")
# get_personal_offset("place")
# get_personal_offset("hover")
get_points("hover")
get_points("place")