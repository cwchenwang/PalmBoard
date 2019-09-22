names = ["luyiqin", "lwk", "wyd", "cai", "czt", "fjy", "wangchen1", "gsh", "fsq", "lc", "lxy", "qdn"]

for name in names:
    for mode in ["hover", "place"]:
        #print(name, mode)
        resp_dict = { 1: [], 2:[], 3:[], 4:[], 5:[] }
        f = open(name+"-"+mode+"-new.txt", 'r')
        for i in range(60):
            line1 = f.readline()[:-1]
            line2 = f.readline()[:-1]
            for i in range(len(line1)):
                finger = line2[i]
                if(finger == " "):
                    finger = 1
                else:
                    finger = int(finger)
                if(resp_dict[finger].__contains__(line1[i].lower()) == False):
                    resp_dict[finger].append(line1[i])
        print(name+","+mode+","+str(len(resp_dict[1]))+","+str(len(resp_dict[2]))+","+str(len(resp_dict[3]))+","+str(len(resp_dict[4]))+","+str(len(resp_dict[5])))
        #     for item in line2:
        #         if(item == " "):
        #             item = 1
        #         if(all.__contains__(int(item))==False):
        #             all.append(int(item))
        # print(name+","+mode+","+str(len(all)))
