import math
import random
import sys
import pickle
import numpy as np

names = [ "fsq", "gsh", "lc", "luyiqin", "lwk", "lxy", "qdn", "wyd", "cai", "czt", "wangchen1", "fjy"]

class Centroid():
    def __init__(self, ux, uy, sx, sy):
        self.ux = ux
        self.uy = uy
        self.sx = sx
        self.sy = sy
    def __str__(self):
        return str(self.ux) + " " + str(self.uy) + " " + str(self.sx) + " " + str(self.sy)

def get_keysize():
    key_size = { "hover": {}, "place": {} }
    with open("keysize.csv") as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1]
            line = line.split(",")
            key_size[line[6]][line[7]] = ( float(line[0]), float(line[3]) )
    return key_size

key_size = get_keysize()

class Bayes:
    def __init__(self, path):
        self.word_dict = {}
        self.all_words = []
        for i in range(21):
            self.word_dict[i] = {}

        self.centroids = {}
        self.path = path
        self.get_words()

    def cal_acc(self, mode, name, t):
        offsetx = 0
        offsety = 0
        if t == "general":
            with open("../../data/offset/offset-"+mode+".csv", "r") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.split(",")
                    if(line[0] == name):
                        offsetx = float(line[2])
                        offsety = float(line[3])
                        break
        print(offsetx, offsety)

        self.get_pos(mode, name, t)

        tot1 = tot2 = tot3 = tot4 = tot5 = 0
        num = 0
        # error_x = error_y = 0
        # all_len = 0
        counter = {}
        for i in range(97, 123):
            counter[chr(i)] = 0
        data = pickle.load(open("/Volumes/Seagate Exp/data/"+mode+"/"+name+"/mapping.pkl", 'rb'))

        words = self.get_per_words("/Volumes/Seagate Exp/data/", mode, name)

        for item in words:
            # if(item != "i"):
            #     continue
            x = []
            y = []
            m_data = []
            for char in item:
                if t == "general":
                    x.append(data[char][counter[char]][0]+offsetx)
                    y.append(data[char][counter[char]][1]+offsety)
                else:
                    x.append(data[char][counter[char]][0])
                    y.append(data[char][counter[char]][1])
                # m_data.append(data[char][counter[char]])
                counter[char] += 1
        # for item in self.all_words:
        #     if num % 1000 == 0 and num != 0:
        #         print(tot1, tot2, tot3, tot4, tot5)
            # num += 1
            # x = []
            # y = []
            # for char in item:
            #     tepx = np.random.normal(loc=self.centroids[char].ux,scale=self.centroids[char].sx)
            #     tepy = np.random.normal(loc=self.centroids[char].uy,scale=self.centroids[char].sy)
            #     x.append(tepx)
            #     y.append(tepy)

            self.latest_x = x
            self.latest_y = y
            result = self.get_candidate(x, y)
            # result = self.get_rel_cand(x, y)
            # print(item, result)
            if(result[0] == item):
                tot1 += 1
            elif(result[1] == item):
                tot2 += 1
            elif(result[2] == item):
                tot3 += 1
            elif(result[3] == item):
                tot4 += 1
            elif(result[4] == item):
                tot5 += 1
            # if(result[0] == item or result[1] == item or result[2] == item or result[3] == item or result[4] == item):
            #     self.update(item)
            # else:
            #     self.update(result[random.randint(0,4)])
        tot2 += tot1
        tot3 += tot2
        tot4 += tot3
        tot5 += tot4
        word_num = len(words)
        # print(tot1, tot2, tot3, tot4, tot5)
        # print(tot1/word_num, tot2/word_num, tot3/word_num, tot4/word_num, tot5/word_num)
        return tot1/word_num, tot2/word_num, tot3/word_num, tot4/word_num, tot5/word_num

    # def cal_acc(self, mode, name):
    #     self.get_pos(mode, name)
    #     tot1 = tot2 = tot3 = tot4 = tot5 = 0
    #     num = 0
    #     # error_x = error_y = 0
    #     # all_len = 0
    #     for item in self.all_words:
    #         if num % 1000 == 0 and num != 0:
    #             print(tot1, tot2, tot3, tot4, tot5)
    #         num += 1
    #         x = []
    #         y = []
    #         for char in item:
    #             tepx = np.random.normal(loc=self.centroids[char].ux,scale=self.centroids[char].sx)
    #             tepy = np.random.normal(loc=self.centroids[char].uy,scale=self.centroids[char].sy)
    #             x.append(tepx)
    #             y.append(tepy)
    #             # error_x += math.erfc((tepx-self.centroids[char].ux)/self.centroids[char].sx)
    #             # error_y += math.erfc((tepx-self.centroids[char].uy)/self.centroids[char].sy)
    #             # print(error_x, error_y)
    #         # all_len += len(item)

    #         result = self.get_candidate(x, y)
    #         print(result, item)
    #         if(result[0] == item):
    #             tot1 += 1
    #         elif(result[1] == item):
    #             tot2 += 1
    #         elif(result[2] == item):
    #             tot3 += 1
    #         elif(result[3] == item):
    #             tot4 += 1
    #         elif(result[4] == item):
    #             tot5 += 1
    #         # print(num, tot1, tot2, tot3, tot4, tot5)
    #     tot2 += tot1
    #     tot3 += tot2
    #     tot4 += tot3
    #     tot5 += tot4
    #     print(tot1, tot2, tot3, tot4, tot5)
    #     word_num = len(self.all_words)
    #     print(tot1/word_num, tot2/word_num, tot3/word_num, tot4/word_num, tot5/word_num)
    #     return tot1/word_num, tot2/word_num, tot3/word_num, tot4/word_num, tot5/word_num

    def get_words(self):
        with open(self.path+"words-10000.csv", 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line[:-1]
                line = line.split(",")
                self.word_dict[len(line[0])][line[0]] = math.log( float(line[1]) )
                self.all_words.append(line[0])
        # for item in self.word_dict:
        #     print(item, self.word_dict[item])

    def get_pos(self, mode, name, t):
        # with open(self.path+name+"-"+mode+"-center.csv", 'r') as f:
        # with open(self.path+"/center/all-center-"+mode+".csv", 'r') as f:
        with open(self.path+name+"-"+mode+"-center.csv", 'r') as f:
            print(mode, name)
            lines = f.readlines()
            for line in lines:
                line = line[:-1]
                line = line.split(",")
                self.centroids[line[0]] = Centroid(float(line[1]), float(line[2]), float(line[3]), float(line[4]))
        # self.oneline()
        self.merge2()
            # for item in self.centroids:
            #     print(self.centroids[item])

    def get_candidate(self, x, y):
        max_prob1 = -sys.float_info.max
        max_prob2 = -sys.float_info.max
        max_prob3 = -sys.float_info.max
        max_prob4 = -sys.float_info.max
        max_prob5 = -sys.float_info.max
        # print(10000 > sys.float_info.min)
        max_word1 = max_word2 = max_word3 = max_word4 = max_word5 = ""
        word_len = len(x)
        # print(x, y)
        for word in self.word_dict[word_len]:
            prob = self.word_dict[word_len][word]
            for i in range(word_len):
                prob += self.cal_psi(word[i], x[i], y[i])
            # print(prob, word)
            if(prob > max_prob1):
                # print("hello")
                max_prob5 = max_prob4
                max_word5 = max_word4
                max_prob4 = max_prob3
                max_word4 = max_word3
                max_prob3 = max_prob2
                max_word3 = max_word2
                max_prob2 = max_prob1
                max_word2 = max_word1
                max_prob1 = prob
                max_word1 = word
            elif(prob > max_prob2):
                max_prob5 = max_prob4
                max_word5 = max_word4
                max_prob4 = max_prob3
                max_word4 = max_word3
                max_prob3 = max_prob2
                max_word3 = max_word2
                max_prob2 = prob
                max_word2 = word
            elif(prob > max_prob3):
                max_prob5 = max_prob4
                max_word5 = max_word4
                max_prob4 = max_prob3
                max_word4 = max_word3
                max_prob3 = prob
                max_word3 = word
            elif(prob > max_prob4):
                max_prob5 = max_prob4
                max_word5 = max_word4
                max_prob4 = prob
                max_word4 = word
            elif(prob > max_prob5):
                max_prob5 = prob
                max_word5 = word
        # print(max_word1, max_word2, max_word3, max_word4, max_word5)
        return [max_word1, max_word2, max_word3, max_word4, max_word5]


    # def cal_pw(self, word):
    #     return self.word_dict[word]
    
    def get_per_words(self, path, mode, name):
        words = []
        with open(path+mode+"/"+name+"/sentences") as f:
            lines = f.readlines()
            for line in lines:
                line = line[:-1]
                line = line.split(" ")
                for word in line:
                    word = word.lower()
                    words.append(word)
        return words

    def cal_psi(self, c, x, y):
        z = math.pow(x-self.centroids[c].ux,2)/math.pow(self.centroids[c].sx,2) + math.pow(y-self.centroids[c].uy, 2)/math.pow(self.centroids[c].sy, 2)
        res = 1/(2*math.pi*self.centroids[c].sx*self.centroids[c].sy)*math.exp(-0.5*z)
        if(res == 0):
            return math.log(1e-300)
        return math.log( 1/(2*math.pi*self.centroids[c].sx*self.centroids[c].sy)*math.exp(-0.5*z) )

    def oneline(self):
        self.centroids['q'].ux = self.centroids['a'].ux = self.centroids['z'].ux = (self.centroids['q'].ux + self.centroids['a'].ux + self.centroids['z'].ux)/3
        self.centroids['w'].ux = self.centroids['s'].ux = self.centroids['x'].ux = (self.centroids['w'].ux + self.centroids['s'].ux + self.centroids['x'].ux)/3
        self.centroids['e'].ux = self.centroids['d'].ux = self.centroids['c'].ux = (self.centroids['e'].ux + self.centroids['d'].ux + self.centroids['c'].ux)/3
        self.centroids['r'].ux = self.centroids['f'].ux = self.centroids['v'].ux = (self.centroids['r'].ux + self.centroids['f'].ux + self.centroids['v'].ux)/3 
        self.centroids['t'].ux = self.centroids['g'].ux = self.centroids['b'].ux = (self.centroids['t'].ux + self.centroids['g'].ux + self.centroids['b'].ux)/3 
        self.centroids['y'].ux = self.centroids['h'].ux = self.centroids['n'].ux = (self.centroids['y'].ux + self.centroids['h'].ux + self.centroids['n'].ux)/3 
        self.centroids['u'].ux = self.centroids['j'].ux = self.centroids['m'].ux = (self.centroids['u'].ux + self.centroids['j'].ux + self.centroids['m'].ux)/3 
        self.centroids['i'].ux = self.centroids['k'].ux = (self.centroids['i'].ux + self.centroids['k'].ux)/2

        self.centroids['q'].uy = self.centroids['a'].uy = self.centroids['z'].uy = (self.centroids['q'].uy + self.centroids['a'].uy + self.centroids['z'].uy)/3
        self.centroids['w'].uy = self.centroids['s'].uy = self.centroids['x'].uy = (self.centroids['w'].uy + self.centroids['s'].uy + self.centroids['x'].uy)/3
        self.centroids['e'].uy = self.centroids['d'].uy = self.centroids['c'].uy = (self.centroids['e'].uy + self.centroids['d'].uy + self.centroids['c'].uy)/3
        self.centroids['r'].uy = self.centroids['f'].uy = self.centroids['v'].uy = (self.centroids['r'].uy + self.centroids['f'].uy + self.centroids['v'].uy)/3 
        self.centroids['t'].uy = self.centroids['g'].uy = self.centroids['b'].uy = (self.centroids['t'].uy + self.centroids['g'].uy + self.centroids['b'].uy)/3 
        self.centroids['y'].uy = self.centroids['h'].uy = self.centroids['n'].uy = (self.centroids['y'].uy + self.centroids['h'].uy + self.centroids['n'].uy)/3 
        self.centroids['u'].uy = self.centroids['j'].uy = self.centroids['m'].uy = (self.centroids['u'].uy + self.centroids['j'].uy + self.centroids['m'].uy)/3 
        self.centroids['i'].uy = self.centroids['k'].uy = (self.centroids['i'].uy + self.centroids['k'].uy)/2

    def merge2(self):

        self.centroids['q'].ux = self.centroids['w'].ux = (self.centroids['q'].ux + self.centroids['w'].ux)/2
        self.centroids['e'].ux = self.centroids['r'].ux = (self.centroids['e'].ux + self.centroids['r'].ux)/2 
        self.centroids['t'].ux = self.centroids['y'].ux = (self.centroids['t'].ux + self.centroids['y'].ux)/2
        self.centroids['u'].ux = self.centroids['i'].ux = (self.centroids['u'].ux + self.centroids['i'].ux)/2
        self.centroids['o'].ux = self.centroids['p'].ux = (self.centroids['o'].ux + self.centroids['p'].ux)/2
        self.centroids['a'].ux = self.centroids['s'].ux = (self.centroids['a'].ux + self.centroids['s'].ux)/2
        self.centroids['d'].ux = self.centroids['f'].ux = (self.centroids['d'].ux + self.centroids['f'].ux)/2
        self.centroids['g'].ux = self.centroids['h'].ux = (self.centroids['g'].ux + self.centroids['h'].ux)/2
        self.centroids['j'].ux = self.centroids['k'].ux = (self.centroids['j'].ux + self.centroids['k'].ux)/2
        self.centroids['z'].ux = self.centroids['x'].ux = (self.centroids['z'].ux + self.centroids['x'].ux)/2
        self.centroids['c'].ux = self.centroids['v'].ux = (self.centroids['c'].ux + self.centroids['v'].ux)/2
        self.centroids['b'].ux = self.centroids['n'].ux = (self.centroids['b'].ux + self.centroids['n'].ux)/2

        multix = 2*key_size[mode][name][0] * 15.1/25.5
        multiy = key_size[mode][name][1] * 10.4/25.5
        # self.centroids['q'].sx = self.centroids['w'].sx = (self.centroids['q'].sx + self.centroids['w'].sx)/2 * multix
        # self.centroids['e'].sx = self.centroids['r'].sx = (self.centroids['e'].sx + self.centroids['r'].sx)/2 * multix
        # self.centroids['t'].sx = self.centroids['y'].sx = (self.centroids['t'].sx + self.centroids['y'].sx)/2 * multix
        # self.centroids['u'].sx = self.centroids['i'].sx = (self.centroids['u'].sx + self.centroids['i'].sx)/2 * multix
        # self.centroids['o'].sx = self.centroids['p'].sx = (self.centroids['o'].sx + self.centroids['p'].sx)/2 * multix
        # self.centroids['a'].sx = self.centroids['s'].sx = (self.centroids['a'].sx + self.centroids['s'].sx)/2 * multix
        # self.centroids['d'].sx = self.centroids['f'].sx = (self.centroids['d'].sx + self.centroids['f'].sx)/2 * multix
        # self.centroids['g'].sx = self.centroids['h'].sx = (self.centroids['g'].sx + self.centroids['h'].sx)/2 * multix
        # self.centroids['j'].sx = self.centroids['k'].sx = (self.centroids['j'].sx + self.centroids['k'].sx)/2 * multix
        # self.centroids['z'].sx = self.centroids['x'].sx = (self.centroids['z'].sx + self.centroids['x'].sx)/2 * multix
        # self.centroids['c'].sx = self.centroids['v'].sx = (self.centroids['c'].sx + self.centroids['v'].sx)/2 * multix
        # self.centroids['b'].sx = self.centroids['n'].sx = (self.centroids['b'].sx + self.centroids['n'].sx)/2 * multix

        # self.centroids['q'].sy = self.centroids['w'].sy = (self.centroids['q'].sy + self.centroids['w'].sy)/2 * multiy
        # self.centroids['e'].sy = self.centroids['r'].sy = (self.centroids['e'].sy + self.centroids['r'].sy)/2 * multiy
        # self.centroids['t'].sy = self.centroids['y'].sy = (self.centroids['t'].sy + self.centroids['y'].sy)/2 * multiy
        # self.centroids['u'].sy = self.centroids['i'].sy = (self.centroids['u'].sy + self.centroids['i'].sy)/2 * multiy
        # self.centroids['o'].sy = self.centroids['p'].sy = (self.centroids['o'].sy + self.centroids['p'].sy)/2 * multiy
        # self.centroids['a'].sy = self.centroids['s'].sy = (self.centroids['a'].sy + self.centroids['s'].sy)/2 * multiy
        # self.centroids['d'].sy = self.centroids['f'].sy = (self.centroids['d'].sy + self.centroids['f'].sy)/2 * multiy
        # self.centroids['g'].sy = self.centroids['h'].sy = (self.centroids['g'].sy + self.centroids['h'].sy)/2 * multiy
        # self.centroids['j'].sy = self.centroids['k'].sy = (self.centroids['j'].sy + self.centroids['k'].sy)/2 * multiy
        # self.centroids['z'].sy = self.centroids['x'].sy = (self.centroids['z'].sy + self.centroids['x'].sy)/2 * multiy
        # self.centroids['c'].sy = self.centroids['v'].sy = (self.centroids['c'].sy + self.centroids['v'].sy)/2 * multiy
        # self.centroids['b'].sy = self.centroids['n'].sy = (self.centroids['b'].sy + self.centroids['n'].sy)/2 * multiy

        # print("before")
        # for item in self.centroids:
        #     print(item, self.centroids[item].sx, self.centroids[item].sy)
        
        for item in self.centroids:
            if(item != 'l' and item != 'm'):
                self.centroids[item].sx = 2*key_size[mode][name][0] * 15.1/25.13
                self.centroids[item].sy = key_size[mode][name][1] * 10.4/(19.05*1.297)

        # print("after")
        # for item in self.centroids:
        #     print(item, self.centroids[item].sx, self.centroids[item].sy)
        
        # for item in self.centroids:
        #     print(item, self.centroids[item].ux, self.centroids[item].uy)
            

# def get_gaussian_points(mu, sigma):
#     return np.random.normal(loc=mu,scale=sigma,size=1)


if __name__ == "__main__":
    bayes = Bayes("../../data/")
    modes = ["place", "hover"]
    f = open("bi-pers-res-new.csv", 'w+')
    f.write("mode,top,name,acc\n")
    for mode in modes:
        for name in names:
            (acc1, acc2, acc3, acc4, acc5) = bayes.cal_acc(mode, name, "personal")
            acc_list=[acc1, acc2, acc3, acc4, acc5]
            print(acc_list)
            for i in range(5):
                f.write(mode+","+str(i)+","+name+","+str(acc_list[i])+"\n")
    f.close()