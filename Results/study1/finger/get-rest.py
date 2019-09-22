def get_sentences(path, mode, name):
    sentences = []
    with open(path+mode+"/"+name+"/sentences") as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1]
            sentences.append(line)
            all = ""
            for item in line:
                if(item == " "):
                    all += "2"
                else:
                    all += "2"
            print(line)
            print(all)

get_sentences("/Volumes/Seagate Exp/data/", "hover", "gsh")
