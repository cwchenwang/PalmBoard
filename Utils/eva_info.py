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
            # words = line.split(" ")
            # for item in words:
            #     answer.append(item)
            i = i + 1
    return answer

def read_result(path):
    result = {}
    with open(path+"result") as f:
        lines = f.readlines()
        i = 0
        for line in lines:
            line = line[1:-2]
            result[i] = line
            # words = line.split(" ")
            # for item in words:
            #     result.append(item)
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
                events[cur].append( (item[2], int(item[1]) ))
            else:
                tep = []
                tep.append((item[2],int(item[1])))
                events[cur] = tep
    return events

modes = ["qwerty", "sensel", "personal"]
# path = "../Debug/data/sensel/lyt/"
names = ["lyt", "zcc", "lry", "jxt", "ljs", "hyx", "zfs", "lwk", "yzj", "cc1"]
#names = ["lyt", "zcc", "lry", "jxt", "hyx", "zfs", "yzj", "cc1", "ljs","lwk"]
#names = ["wc"]
# names = ["lyt", "jxt", "zcc", "zfs"]
#names = ["zfs"]
TOTWORDS = 179

sub = 0
for mode in modes:
    
    for name in names:
        last_event = ""
        path = "../Debug/data/" + mode + "/" + name + "/"
        clear_dict = get_clear(path)
        result = read_result(path)
        answer = get_answer(path)
        events = get_events(path, clear_dict)
        # print(events)
        
        match_yes = 0
        match_no = 0
        slct_yes = 0
        slct_no = 0
        undo = 0
        delete = 0

        for i in range(len(result)):
            event = events[i]
            rs_cnt = 0
            res = result[i].split(" ")
            ans = answer[i].split(" ")
            cur_word = 0
            ctct_cnt = 0
            last_event = ""
            for te in event:
                e = te[0]
                if(e == "new"):
                    ctct_cnt += 1
                if(e == "leftswipe"):
                    if(last_event == "new"):
                        undo += 1
                    elif(last_event == "confirm"):
                        delete += 1
                        cur_word = cur_word - 1
                    elif(last_event == "leftswipe"):
                        delete += 1
                        cur_word = cur_word - 1
                    ctct_cnt = 0
                if(e == "rightswipe"):
                    rs_cnt += 1
                if(e == "confirm"):
                    if(rs_cnt == 0 and last_event == "new"):
                        if(ans.__contains__(res[cur_word])):
                            match_yes += 1
                        else:
                            match_no += 1
                    elif(ctct_cnt > 0):
                        if(ans.__contains__(res[cur_word])):
                            slct_yes += 1
                        else:
                            slct_no += 1
                    rs_cnt = 0
                    if(last_event == "new" or last_event == "rightswipe"):
                        # print(res[cur_word], te[1])

                        cur_word += 1
                        
                        # print(name, mode, "add", i, cur_word, result[i])
                        
                last_event = e

            # print(match_yes, match_no, slct_yes, slct_no, undo, delete)
        tot = 0
        tot += match_yes
        tot += match_no
        tot += slct_yes
        tot += slct_no
        tot += undo
        tot += delete
        # print(tot)
        print(name+","+mode+","+str(match_yes/tot)+","+str(match_no/tot)+","+str(slct_yes/tot)+","+str(slct_no/tot)+","+str(undo/tot)+","+str(delete/tot))



        # print(events)
        # for i in len(result)
#         # calculate word level error rate
#         # if(len(result) != len(answer)):
#         #     print(name, mode)
#         # if(name == "jxt" and mode == "personal"):
#         #     print(len(result))
#         i = 0
#         tot_words = 0
#         error_num = 0
#         for r, a in zip(result, answer):
#             # if(len(result[r]) < 3):
#                 # print(name, mode, r, answer[a])
#             re = result[r].split(" ")
#             an = answer[a].split(" ")
#             if(len(re) != len(an)):
#                 pass
# #                print(re, an, name, mode)
#             else:
#                 tot_words += len(an)
#                 for w1, w2 in zip(re, an):
#                     if(w1 != w2):
#                         error_num +=1
#                         # print(name, mode, w1, w2)
#             i = i + 1
#             if(i % 8 == 0):
#                 print(str(error_num)+","+str(tot_words)+","+name+","+mode+","+str(int(i/8))+","+str(error_num/tot_words)+","+str(1-error_num/tot_words))
#                 tot_words = 0
#                 error_num = 0


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
