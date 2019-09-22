from cer import cer

def get_clear(path): 
    clear_dict = {}
    with open(path+"clear") as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1]
            line = line.split(" ")
            clear_dict[int(line[0])] = int(line[3])
    return clear_dict

def get_answer(path):
    answer = {}
    with open(path+"sentences") as f:
        lines = f.readlines()
        i = 0
        for line in lines:
            line = line[:-1]
            answer[i] = line
            i = i + 1
    return answer

def read_result(path):
    result = {}
    words = []
    with open(path+"result") as f:
        lines = f.readlines()
        i = 0
        for line in lines:
            line = line[1:-2]
            result[i] = line
            i = i + 1
            # line = line.split(" ")
            # for item in line:
            #     words.append(item)
    # print(len(words))
    # print(words)
    return result

def get_events(path, clear):
    events = {}
    cur = 0
    with open(path+"log") as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1]
            item = line.split(" ")
#            print(item[0])
            if(int(item[0]) != cur):
                cur = int(item[0])
            if(clear.__contains__(cur)):
                if(int(item[1]) < clear[cur]):
                    continue
            if(events.__contains__(cur)):
                events[cur].append(int(item[1]))
            else:
                tep = []
                tep.append(int(item[1]))
                events[cur] = tep
    return events

modes = ["qwerty", "sensel", "personal"]
# path = "../Debug/data/sensel/lyt/"
names = ["lyt", "zcc", "lry",  "jxt", "ljs", "hyx", "zfs", "lwk", "yzj", "cc1"]
#names = ["lyt", "zcc", "lry", "jxt", "hyx", "zfs", "yzj", "cc1", "ljs","lwk"]
#names = ["wc"]
# names = ["lyt", "jxt", "zcc", "zfs"]
#names = ["zfs"]
TOTWORDS = 179

sub = 0
f = open("cer-all.csv", 'w')
f.write("name, mode, blk, cer\n")
for name in names:
    for mode in modes:
        tot_sentences = 0
        tot_cer = 0
        path = "/Users/clarencewang/Desktop/sensel-typing/Debug/data/" + mode + "/" + name + "/"
        clear_dict = get_clear(path)
        result = read_result(path)
        answer = get_answer(path)

        # calculate character level error rate
        for r, a in zip(result, answer):
            tot_cer += cer(answer[a], result[r])
            tot_sentences += 1
            if(tot_sentences % 8 == 0):
                f.write(name+","+mode+","+str(tot_sentences/8)+","+str(tot_cer/8)+"\n")
                tot_cer = 0
                #tot_sentences = 0
            # if(cer(answer[a], result[r]) > 0.1):
            #     print(answer[a], result[r], cer(answer[a], result[r]))

        # calculate word level error rate
        i = 0
        tot_words = 0
        error_num = 0
        for r, a in zip(result, answer):
            # if(len(result[r]) < 3):
                # print(name, mode, r, answer[a])
            re = result[r].split(" ")
            an = answer[a].split(" ")
            if(len(re) != len(an)):
                pass
#                print(re, an, name, mode)
            else:
                tot_words += len(an)
                for w1, w2 in zip(re, an):
                    if(w1 != w2):
                        error_num +=1
                        print(name, mode, int(i/8), w1, w2)
            i = i + 1
            if(i % 8 == 0):
                # print(str(error_num)+","+str(tot_words)+","+name+","+mode+","+str(int(i/8))+","+str(error_num/tot_words)+","+str(1-error_num/tot_words))
                tot_words = 0
                error_num = 0


    #     events = get_events(path, clear_dict)
    #     # print(result, events)
    #     # print(result)
    #     time = 0
    #     char = 0
    #     i = 0
    # #    print(result)
    #     for r, e in zip(result, events):
    #         # print(i, r)
    #         i = i + 1
    #         # print((events[e][-1] - events[e][0])/1000, len(r))
    #         if(i % 8 == 0):
    #             print( name+","+str(int(i/8))+","+ mode + "," + str(char/(time/1000)/5*60))
    #             time = 0
    #             char = 0
    #         time += events[e][-1] - events[e][0]
    #         # print(time)
    #         char += len(result[r])
    # sub += 1
#print(char/(time/1000)/5*60)
f.close()
