
tot_words = 0
tot_times = 0
word_dict = {}
max_len = 0

def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
            return True
    else:
            return False


#print(tot_frequency)

# testset = open("testset.txt", 'w')
modes = ["hover", "place"]
names = ["wangchen1", "cai", "luyiqin", "fjy", "lc",  "lwk", "lxy", "qdn", "wyd", 'czt', "gsh", "fsq"]
path = "/Volumes/Seagate Exp/data/"

words = {}
def get_words(path, mode, name):
    counter = {}
    for i in range(97, 123):
        counter[chr(i)] = 0
    with open(path+mode+"/"+name+"/sentences") as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1]
            line = line.split(" ")
            for word in line:
                word = word.lower()
                if(words.__contains__(word) == False):
                    words[word] = 0

for mode in modes:
    for name in names:
        get_words(path, mode, name)

counter = 0
with open("ANC-token-count.txt", 'r', encoding="ISO-8859-1") as f:
    for line in f:
        # print(line)
        line = line.split("\t")
        if(len(line[0]) > max_len):
            max_len = len(line[0])
        is_word = True
        for char in line[0]:
            if is_alphabet(char) == False:
                is_word = False
                # print("no word", line[0])
                break
        if is_word:
            if(line[0] == "gas"):
                word_dict[line[0]] = 2000
                tot_times += 2000
            else:
                if(tot_words >= 10000):
                    if(words.__contains__(line[0]) and words[line[0]] == 0):
                        words[line[0]] = int(line[1])
                        word_dict[line[0]] = int(line[1])
                        tot_times += int(line[1])
                        counter += 1
                else:
                    word_dict[line[0]] = int(line[1])
                    tot_times += int(line[1])
            tot_words += 1
            if(counter == len(words)):
                break
        # if(tot_words >= 10000):
        #     if()
        #     break
# print(max_len)
print(len(word_dict))
tot_frequency = 0
# word_dict["seven"] = 17
# word_dict["dipped"] = 66
# word_dict["zero"] = 107
# word_dict["discreet"] = 52

words_file = open("words-train.csv", 'w')
for item in word_dict:
    word_dict[item] = word_dict[item]/tot_times
    # print(item, word_dict[item])
    tot_frequency += word_dict[item]
    words_file.write(item + "," + str(word_dict[item])+","+str(len(item))+"\n")
words_file.close()

# with open("T-40.txt", 'r') as f:
#     for line in f:
#         line = line[:-1]
#         phrase = line
#         line = line.split(" ")
#         valid = True
#         for item in line: 
#             if(word_dict.__contains__(item.lower())):
#                 continue
#             else:
#                 print(item)
#                 valid = False
#         if valid == False:
#             print(phrase)
            # testset.write(phrase+"\n")

# testset.close()
