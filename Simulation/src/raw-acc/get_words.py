import numpy as np
import pickle
import sys


def get_words(path, mode, name):
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

def get_sentences(path, mode, name):
    sentences = []
    with open(path+mode+"/"+name+"/sentences") as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1]
            sentences.append(line)
    return sentences

def get_sd(path, mode, name, sentences, f):
    counter = {}
    for i in range(97, 123):
        counter[chr(i)] = 0
    counter[' '] = 0
    data = pickle.load(open(path+mode+"/"+name+"/mapping.pkl", 'rb'))
    charx = []
    chary = []
    spacex = []
    spacey = []
    num_sent = 0
    tot_char = 0
    tot_time = 0
    for sentence in sentences:
        for i in range(len(sentence)):
            char = sentence[i]
            char = char.lower()
            if(char == ' '):
                spacex.append(data[char][counter[char]][0])
                spacey.append(data[char][counter[char]][1])
            else:
                charx.append(data[char][counter[char]][0])
                chary.append(data[char][counter[char]][1])
            counter[char] += 1
        num_sent += 1
        if(num_sent % 15 == 0):
            print(len(charx), len(chary), len(spacex), len(spacey))
            # print(name, mode, num_sent/15, np.std(charx)*1.319, np.std(chary)*1.297, np.std(spacex)*1.319, np.std(spacey)*1.297)
            f.write(name+","+mode+","+str(int(num_sent/15))+","+str(np.std(charx)*1.319)+","+str(np.std(chary)*1.297)+","+str(np.std(spacex)*1.319)+","+str(np.std(spacey)*1.297)+"\n")
            charx = []
            chary = []
            spacex = []
            spacey = []

def get_points(path, mode, name, words):
    counter = {}
    for i in range(97, 123):
        counter[chr(i)] = 0
    data = pickle.load(open(path+mode+"/"+name+"/mapping-contacts.pkl", 'rb'))
    
    for word in words:
        x = []
        y = []
        for char in word:
            x.append(data[char][counter[char]])
            y.append(data[char][counter[char]])
            counter[char] += 1
        print(word, x, y)

# words = get_words("/Volumes/Seagate Exp/data/", "place", "wangchen1")
# get_points("/Volumes/Seagate Exp/data/", "place", "wangchen1", words)
# sentences = get_sentences("/Volumes/Seagate Exp/data/", "place", "wangchen1")
# get_sd("/Volumes/Seagate Exp/data/", "place", "wangchen1", sentences)
names = ["wangchen1", "cai", "luyiqin", "fjy", "lc",  "lwk", "lxy", "qdn", "wyd", 'czt', "gsh", "fsq"]

f = open("key-std.csv", 'w')
f.write("subject,mode,block,sdx,sdy,sdxspace,sdyspace,speed\n")
for name in names:
    for mode in ["hover", "place"]:
        sentences = get_sentences("/Volumes/Seagate Exp/data/", mode, name)
        get_sd("/Volumes/Seagate Exp/data/", mode, name, sentences, f)
f.close()