with open("all.csv", 'r') as f:
    lines = f.readlines()
    f.readline()
    for line in lines:
        line = line[:-1]
        line = line.split(",")
        line[0] = str(float(line[0])*1.319)
        line[1] = str(float(line[1])*1.297)
        line[3] = str(float(line[3])*1.319)
        line[4] = str(float(line[4])*1.297)

        for i in range(len(line)):
            if(i != len(line) - 1):
                print(line[i]+",", end="")
            else:
                print(line[i])