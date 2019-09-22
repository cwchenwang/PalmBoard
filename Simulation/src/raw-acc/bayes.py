import math
import random
import sys
import pickle
import numpy as np
from sklearn.model_selection import train_test_split  # 数据分区库
from sklearn import tree  # 导入决策树库
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, auc, confusion_matrix, f1_score, precision_score, recall_score, \
    roc_curve  # 导入指标库

#"wangchen1", "cai",
names = ["cai", "luyiqin", "fjy", "lc",  "lwk", "lxy", "qdn", "wyd", 'czt', "gsh", "fsq", "wangchen1"]
# names = ["wangchen1", "cai"]

abs_pos = { 'q': [0,2], 'w': [1,2], 'e': [2,2], 'r': [3,2], 't':[4,2], 'y':[5,2], 'u':[6,2], 'i':[7,2], 'o':[8,2], 'p':[9,2], 'a':[0.25, 1], 's':[1.25,1], 'd':[2.25,1], 'f':[3.25,1], 'g':[4.25,1], 'h':[5.25,1], 'j':[6.25,1], 'k':[7.25,1], 'l':[8.25,1], 'z':[0.75, 0], 'x':[1.75,0], 'c':[2.75,0], 'v':[3.75,0], 'b':[4.75, 0], 'n':[5.75, 0], 'm': [6.75, 0] }

char_row = { "q": 1, "w": 1, "e": 1, "r": 1, "t": 1, "y": 1, "u": 1, "i": 1, "o": 1, "p": 1, "a": 0, "s": 0, "d": 0, "f": 0, "g": 0, "h": 0, "j": 0, "k": 0, "l": 0, "z": -1, "x": -1, "c": -1, "v": -1, "b": -1, "n": -1, "m": -1, " ": -2}

class Centroid():
    def __init__(self, ux, uy, sx, sy):
        self.ux = ux
        self.uy = uy
        self.sx = sx
        self.sy = sy
    def __str__(self):
        return str(self.ux) + " " + str(self.uy) + " " + str(self.sx) + " " + str(self.sy)

class Bayes:
    def __init__(self, path, session="personal"):
        self.session = session
        self.word_dict = {}
        self.all_words = []
        for i in range(21):
            self.word_dict[i] = {}

        self.centroids = {}
        self.rela_center = {}
        self.path = path
        self.latest_x = []
        self.latest_y = []
        self.get_words()

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

    def get_clf(self, mode, name):
        raw_data = np.loadtxt('/Users/clarencewang/Desktop/HCI/sensel/sensel-finger-typing/src/utils/all-ct-'+name+"-"+mode+
       '.csv', delimiter=',', skiprows=1, )  # 读取数据文件
        X = raw_data[:,3:9]  # 分割X
        y = raw_data[:,1]  # 分割y
        clf = GaussianNB()
        clf.fit(X, y)
        return clf

    def cal_acc_with_force(self, mode, name, t):
        self.get_pos(mode, name)
        self.get_rel_pos(mode, name)
        clf = self.get_clf(mode, name)
        counter = {}
        for i in range(97, 123):
            counter[chr(i)] = 0
        data = pickle.load(open("/Volumes/Seagate Exp/data/"+mode+"/"+name+"/mapping-contacts.pkl", 'rb'))

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
        # print(offsetx, offsety)

        tot1 = tot2 = tot3 = tot4 = tot5 = 0
        num = 0

        words = self.get_per_words("/Volumes/Seagate Exp/data/", mode, name)

        for item in words:
            x = []
            y = []
            m_data = []
            for char in item:
                # if t == "general":
                #     x.append(data[char][counter[char]][0]+offsetx)
                #     y.append(data[char][counter[char]][1]+offsety)
                # else:
                #     x.append(data[char][counter[char]][0])
                #     y.append(data[char][counter[char]][1])
                m_data.append(data[char][counter[char]])
                counter[char] += 1

            self.latest_x = x
            self.latest_y = y
            # result = self.get_candidate(x, y)
            # result = self.get_rel_cand(x, y)
            # print(item)
            # for i in range(len(item)):
            #     pred_y = clf.predict_log_proba( [[ m_data[i].x, m_data[i].y, m_data[i].pixels, m_data[i].max_force, m_data[i].avg_force, (m_data[i].ets - m_data[i].sts) ]] )
            #     print(pred_y)

            result = self.get_rel_cand_with_force(m_data, clf, item, offsetx, offsety)
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

        tot2 += tot1
        tot3 += tot2
        tot4 += tot3
        tot5 += tot4
        word_num = len(words)
        return tot1/word_num, tot2/word_num, tot3/word_num, tot4/word_num, tot5/word_num

    # def get_points(self, mode, name):
    #     self.get_pos(mode, name)
    #     clf = self.get_clf(mode, name)
    #     counter = {}
    #     for i in range(97, 123):
    #         counter[chr(i)] = 0
    #     data = pickle.load(open("/Volumes/Seagate Exp/data/"+mode+"/"+name+"/mapping-contacts.pkl", 'rb'))

    #     tot1 = tot2 = tot3 = tot4 = tot5 = 0

    #     words = self.get_per_words("/Volumes/Seagate Exp/data/", mode, name)

    #     for item in words:
    #         x = []
    #         y = []
    #         m_data = []
    #         for char in item:
    #             x.append(data[char][counter[char]][0])
    #             y.append(data[char][counter[char]][1])
    #             m_data.append(data[char][counter[char]])
    #             counter[char] += 1
    #         # print(item, x, y)
    #         # self.latest_x = x
    #         # self.latest_y = y

    #         # result = self.get_candidate(x, y)
    #         result = self.get_pred_cand(m_data, clf, item)
    #         # result = self.get_rel_cand(x, y)
    #         # print(item, result)
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
    #         # if(result[0] == item or result[1] == item or result[2] == item or result[3] == item or result[4] == item):
    #             # self.update(item)
    #     tot2 += tot1
    #     tot3 += tot2
    #     tot4 += tot3
    #     tot5 += tot4
    #     word_num = len(words)
    #     print(tot1, tot2, tot3, tot4, tot5)
    #     # print(tot1/word_num, tot2/word_num, tot3/word_num, tot4/word_num, tot5/word_num)
    #     return tot1/word_num, tot2/word_num, tot3/word_num, tot4/word_num, tot5/word_num

    def cal_acc(self, mode, name, t):
        self.get_pos(mode, name)
        self.get_rel_pos(mode, name)

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
        # print(offsetx, offsety)

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
            # result = self.get_candidate(x, y)
            result = self.get_rel_cand(x, y)
            print(item, result)
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

        tot2 += tot1
        tot3 += tot2
        tot4 += tot3
        tot5 += tot4
        word_num = len(words)
        return tot1/word_num, tot2/word_num, tot3/word_num, tot4/word_num, tot5/word_num

    def get_words(self):
        with open(self.path+"words-train.csv", 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line[:-1]
                line = line.split(",")
                self.word_dict[len(line[0])][line[0]] = math.log( float(line[1]) )
                self.all_words.append(line[0])
        # for item in self.word_dict:
        #     print(item, self.word_dict[item])

    def get_pos(self, mode, name):
        # with open(self.path+name+"-"+mode+"-center.csv", 'r') as f:
        with open(self.path+"/center/all-center-place.csv", 'r') as f:
            # print(mode, name)
            lines = f.readlines()
            for line in lines:
                line = line[:-1]
                line = line.split(",")
                self.centroids[line[0]] = Centroid(float(line[1]), float(line[2]), float(line[3]), float(line[4]))
        
    def get_rel_pos(self, mode, name):
        # with open(self.path+name+"-"+mode+"-rela.csv", 'r') as f:
        with open(self.path+"all-rela.csv", 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line[:-1]
                line = line.split(",")
                self.rela_center[line[0]] = (float(line[1]), float(line[2]))
            # for item in self.centroids:
            #     print(self.centroids[item])

    def get_rel_cand(self, x, y):
        max_prob1 = -sys.float_info.max
        max_prob2 = -sys.float_info.max
        max_prob3 = -sys.float_info.max
        max_prob4 = -sys.float_info.max
        max_prob5 = -sys.float_info.max
        # print(10000 > sys.float_info.min)
        max_word1 = max_word2 = max_word3 = max_word4 = max_word5 = ""
        word_len = len(x)
        for word in self.word_dict[word_len]:
            prob = self.word_dict[word_len][word]
            prob += self.cal_psi(word[0], x[0], y[0])
            for i in range(1, word_len):
                prob += self.cal_rel_psi(word[i-1]+word[i], x[i]-x[i-1], y[i]-y[i-1])
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

    def get_rel_cand_with_force(self, data, clf, answer, offsetx, offsety):
        max_prob1 = -sys.float_info.max
        max_prob2 = -sys.float_info.max
        max_prob3 = -sys.float_info.max
        max_prob4 = -sys.float_info.max
        max_prob5 = -sys.float_info.max
        # print(10000 > sys.float_info.min)
        max_word1 = max_word2 = max_word3 = max_word4 = max_word5 = ""
        word_len = len(data)

                # pred_y = clf.predict_log_proba( [data[i].x, data[i].y, data[i].pixels, data[i].max_force, data[i].avg_force, (data[i].ets - data[i].sts) ])
                # if(char_row(word[i]) == -1):
                #     prob += pred_y[0][0]
                # elif(char_row(word[i]) == 0):
                #     prob += pred_y[0][1]
                # elif(char_row(word[i]) == 1):
                #     prob += pred_y[0][2]
        for word in self.word_dict[word_len]:
            prob = self.word_dict[word_len][word]
            prob += self.cal_psi(word[0], data[0].x+offsetx, data[0].y+offsety)
            for i in range(1, word_len):
                prob += self.cal_rel_psi(word[i-1]+word[i], data[i].x - data[i-1].x, data[i].y-data[i-1].y)

            for i in range(word_len):
                pred_y = clf.predict_log_proba( [[ data[i].x, data[i].y, data[i].pixels, data[i].max_force, data[i].avg_force, (data[i].ets - data[i].sts) ]] )

                # if(answer == "snow"):
                #     print(pred_y, word)
                # if(char_row[word[i]] == char_row[answer[i]]):
                #     prob += 0
                # else:
                #     prob += -100000
                if(char_row[word[i]] == -2):
                    prob += pred_y[0][0]
                elif(char_row[word[i]] == -1):
                    prob += pred_y[0][1]
                elif(char_row[word[i]] == 0):
                    prob += pred_y[0][2]
                elif(char_row[word[i]] == 1):
                    prob += pred_y[0][3]

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

    def get_cand_with_force(self, data, clf):
        max_prob1 = -sys.float_info.max
        max_prob2 = -sys.float_info.max
        max_prob3 = -sys.float_info.max
        max_prob4 = -sys.float_info.max
        max_prob5 = -sys.float_info.max
        # print(10000 > sys.float_info.min)
        max_word1 = max_word2 = max_word3 = max_word4 = max_word5 = ""
        word_len = len(data)

                # pred_y = clf.predict_log_proba( [data[i].x, data[i].y, data[i].pixels, data[i].max_force, data[i].avg_force, (data[i].ets - data[i].sts) ])
                # if(char_row(word[i]) == -1):
                #     prob += pred_y[0][0]
                # elif(char_row(word[i]) == 0):
                #     prob += pred_y[0][1]
                # elif(char_row(word[i]) == 1):
                #     prob += pred_y[0][2]

        for word in self.word_dict[word_len]:
            prob = self.word_dict[word_len][word]
            for i in range(word_len):
                prob += self.cal_psi(word[i], data[i].x, data[i].y)

        # for word in self.word_dict[word_len]:
        #     prob = self.word_dict[word_len][word]
        #     prob += self.cal_psi(word[0], data[0].x, data[0].y)
            # for i in range(1, word_len):
            #     prob += self.cal_rel_psi(word[i-1]+word[i], data[i].x - data[i-1].x, data[i].y-data[i-1].y)

            for i in range(word_len):
                pred_y = clf.predict_log_proba( [[ data[i].x, data[i].y, data[i].pixels, data[i].max_force, data[i].avg_force, (data[i].ets - data[i].sts) ]] )

                # if(answer == "snow"):
                #     print(pred_y, word)
                # if(char_row[word[i]] == char_row[answer[i]]):
                #     prob += 0
                # else:
                #     prob += -100000
                if(char_row[word[i]] == -2):
                    prob += pred_y[0][0]
                elif(char_row[word[i]] == -1):
                    prob += pred_y[0][1]
                elif(char_row[word[i]] == 0):
                    prob += pred_y[0][2]
                elif(char_row[word[i]] == 1):
                    prob += pred_y[0][3]

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

    def get_candidate(self, x, y):
        max_prob1 = -sys.float_info.max
        max_prob2 = -sys.float_info.max
        max_prob3 = -sys.float_info.max
        max_prob4 = -sys.float_info.max
        max_prob5 = -sys.float_info.max
        # print(10000 > sys.float_info.min)
        max_word1 = max_word2 = max_word3 = max_word4 = max_word5 = ""
        word_len = len(x)
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

    def cal_rel_psi(self, c, x, y):
        key_x = "x" + str(int(abs_pos[c[1]][0] - abs_pos[c[0]][0]))
        key_y = "y" + str(int(abs_pos[c[1]][1] - abs_pos[c[0]][1]))
        z = math.pow(x-self.rela_center[key_x][0],2)/math.pow(self.rela_center[key_x][1],2) + math.pow(y-self.rela_center[key_y][0], 2)/math.pow(self.rela_center[key_y][1], 2)
        res = 1/(2*math.pi*self.rela_center[key_x][1]*self.rela_center[key_y][1])*math.exp(-0.5*z)

        if(res == 0):
            return math.log(1e-300)
        return math.log( 1/(2*math.pi*self.rela_center[key_x][1]*self.rela_center[key_y][1])*math.exp(-0.5*z) )

    def cal_psi(self, c, x, y):
        z = math.pow(x-self.centroids[c].ux,2)/math.pow(self.centroids[c].sx,2) + math.pow(y-self.centroids[c].uy, 2)/math.pow(self.centroids[c].sy, 2)
        res = 1/(2*math.pi*self.centroids[c].sx*self.centroids[c].sy)*math.exp(-0.5*z)
        if(res == 0):
            return math.log(1e-300)
        return math.log( 1/(2*math.pi*self.centroids[c].sx*self.centroids[c].sy)*math.exp(-0.5*z) )

    def update(self, word):
        for char, i in zip(word, range(len(word))):
            last_x = self.centroids[char].ux
            last_y = self.centroids[char].uy
            self.centroids[char].ux = self.centroids[char].ux + (self.latest_x[i] - self.centroids[char].ux) * 1.0
            self.centroids[char].uy = self.centroids[char].uy + (self.latest_y[i] - self.centroids[char].uy) * 1.0
            # print(self.centroids[char].sx*self.centroids[char].sx + (self.latest_x[i] - last_x)*(self.latest_x[i]-self.centroids[char].ux))
            # print(self.centroids[char].sy*self.centroids[char].sy + (self.latest_y[i] - last_y)*(self.latest_y[i]-self.centroids[char].uy))
            # self.centroids[char].sx = math.sqrt( self.centroids[char].sx*self.centroids[char].sx + (self.latest_x[i] - last_x)*(self.latest_x[i]-self.centroids[char].ux) )
            # self.centroids[char].sy = math.sqrt( self.centroids[char].sy*self.centroids[char].sy + (self.latest_y[i] - last_y)*(self.latest_y[i]-self.centroids[char].uy) )
# def get_gaussian_points(mu, sigma):
#     return np.random.normal(loc=mu,scale=sigma,size=1)


if __name__ == "__main__":
    bayes = Bayes("../../data/")
    filename = input("Please input file name: ")
    modes = ["hover", "place"]
    f = open(filename+".csv", 'w+')
    f.write("mode,top,name,acc\n")
    for name in names:
        all_acc = [0,0,0,0,0]
        for mode in modes:
            (acc1, acc2, acc3, acc4, acc5) = bayes.cal_acc_with_force(mode, name, "general")
            # (acc1, acc2, acc3, acc4, acc5) = bayes.get_points(mode, name)
            acc_list=[acc1, acc2, acc3, acc4, acc5]
            for i in range(5):
                all_acc[i] += acc_list[i]
            print(name, mode, acc_list)
            for i in range(5):
                print(mode+","+str(i)+","+name+","+str(acc_list[i])+"\n")
        # for i in range(5):
        #     f.write(print(str(i)+","+name+","+str(all_acc[i]/2)+"\n"))
    f.close()