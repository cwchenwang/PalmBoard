import scipy.stats
import numpy as np
import pickle
import math
# key_size = { "hover": {}, "place": {} }

# centroids = {}
qwerty = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"]

class Centroid():
    def __init__(self, ux, uy, sx, sy):
        self.ux = ux
        self.uy = uy
        self.sx = sx
        self.sy = sy
    def __str__(self):
        return str(self.ux) + " " + str(self.uy) + " " + str(self.sx) + " " + str(self.sy)

names = [ "fsq", "gsh", "lc", "luyiqin", "lwk", "lxy", "qdn", "wyd", "cai", "czt", "wangchen1", "fjy"]

# for mode in ["hover", "place"]:
#     for name in names:

def get_centroids(name, mode):
    centroids = {}
    with open("../../data/"+name+"-"+mode+"-center.csv", 'r') as f:
        # print(mode, name)
        lines = f.readlines()
        for line in lines:
            line = line[:-1]
            line = line.split(",")
            centroids[line[0]] = Centroid(float(line[1]), float(line[2]), float(line[3]), float(line[4]))
    return centroids

def get_keysize():
    key_size = { "hover": {}, "place": {} }
    with open("keysize.csv") as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1]
            line = line.split(",")
            key_size[line[6]][line[7]] = ( float(line[0]), float(line[3]) )
    return key_size

def merge2(centroids):
    centroids['q'].ux = centroids['w'].ux = (centroids['q'].ux + centroids['w'].ux)/2
    centroids['e'].ux = centroids['r'].ux = (centroids['e'].ux + centroids['r'].ux)/2 
    centroids['t'].ux = centroids['y'].ux = (centroids['t'].ux + centroids['y'].ux)/2
    centroids['u'].ux = centroids['i'].ux = (centroids['u'].ux + centroids['i'].ux)/2
    centroids['o'].ux = centroids['p'].ux = (centroids['o'].ux + centroids['p'].ux)/2
    centroids['a'].ux = centroids['s'].ux = (centroids['a'].ux + centroids['s'].ux)/2
    centroids['d'].ux = centroids['f'].ux = (centroids['d'].ux + centroids['f'].ux)/2
    centroids['g'].ux = centroids['h'].ux = (centroids['g'].ux + centroids['h'].ux)/2
    centroids['j'].ux = centroids['k'].ux = (centroids['j'].ux + centroids['k'].ux)/2
    centroids['z'].ux = centroids['x'].ux = (centroids['z'].ux + centroids['x'].ux)/2
    centroids['c'].ux = centroids['v'].ux = (centroids['c'].ux + centroids['v'].ux)/2
    centroids['b'].ux = centroids['n'].ux = (centroids['b'].ux + centroids['n'].ux)/2

    for item in centroids:
        if(item != 'l' and item != 'm'):
            centroids[item].sx = 2*key_size[mode][name][item][0] * 15.1/25.5
            centroids[item].sy = key_size[mode][name][item][1] * 10.4/25.5

    return centroids

path = "/Users/clarencewang/Desktop/sensel-typing/Debug/data/"

key_size = get_keysize()
for mode in ["place"]:
    for name in names:
        # print(mode, name)
        data = pickle.load(open(path+mode+"/"+name+"/"+"mapping.pkl", 'rb'))
        center = {}
        # x = data['q'][:,0]
        # y = data['q'][:,1]
        # x = data['q'][:,0]/len(x)
        # y = data['q'][:,1]/len(y)
        # print(x,y)
        center['q'] = (np.sum(data['q'][:,0])/len(data['q'][:,0]), data['q'][:,1]/len(data['q'][:,0]))
        center['t'] = (np.sum(data['t'][:,0])/len(data['t'][:,0]), data['t'][:,1]/len(data['t'][:,0]))
        center['y'] = (np.sum(data['y'][:,0])/len(data['y'][:,0]), data['y'][:,1]/len(data['y'][:,0]))
        center['p'] = (np.sum(data['p'][:,0])/len(data['p'][:,0]), data['p'][:,1]/len(data['p'][:,0]))
        qt = center['t'][0] - center['q'][0]
        py = center['p'][0] - center['y'][0]
        print(str(qt)+","+str(py)+","+str(py/qt))

        # for i in range(len(qwerty)):
        #     char = qwerty[i]
        #     x = data[char][:,0]
        #     y = data[char][:,1]
            # cov = np.cov(data[char], rowvar=0)
            # # print(cov)
            # a,b=np.linalg.eig(cov)
            # # print(a,b)
            # arc = 0
            # if(b[0][0] > 0 and b[1][0] > 0):
            #     if(b[0][1] > 0):
            #         arc = math.atan(b[0][1]/b[0][0])
            #     else:
            #         arc = math.atan(b[1][1]/b[1][0])
            #     # print(arc)
            # elif(b[0][1] > 0 and b[1][1] > 0):
            #     if(b[0][0] < 0):
            #         arc = math.atan(b[0][1]/b[0][0])
            #     else:
            #         arc = math.atan(b[1][1]/b[1][0])
            #     # print(arc)
            #     arc = arc + 3.1415
            
            # print(str(arc)+","+str(i)+","+name)

                    # for i in range(97, 123):
        #     char = chr(i)
        #     centroids = get_centroids(name, mode)
        #     # centroids = merge2(centroids)
        #     # print(centroids[char].ux, centroids[char].sx)
        #     # print(key_size[mode][person][0])
        #     px = scipy.stats.norm(centroids[char].ux, centroids[char].sx).cdf(centroids[char].ux + key_size[mode][name][0]/2) - scipy.stats.norm(centroids[char].ux, centroids[char].sx).cdf(centroids[char].ux - key_size[mode][name][0]/2)
        #     py = scipy.stats.norm(centroids[char].uy, centroids[char].sy).cdf(centroids[char].uy + key_size[mode][name][1]/2) - scipy.stats.norm(centroids[char].uy, centroids[char].sy).cdf(centroids[char].uy - key_size[mode][name][1]/2)
        #     print(mode+","+name+","+str(px)+","+str(py)+","+char+",bi")