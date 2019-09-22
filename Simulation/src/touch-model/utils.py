
abs_pos_arc = { 'q': [0,2], 'w': [1,2.2], 'e': [2,2.4], 'r': [3,2.5], 't':[4,2.5], 'y':[5,2.5], 'u':[6,2.5], 'i':[7,2.4], 'o':[8,2.2], 'p':[9,2], 'a':[0.25, 1], 's':[1.25,1], 'd':[2.25,1], 'f':[3.25,1], 'g':[4.25,1], 'h':[5.25,1], 'j':[6.25,1], 'k':[7.25,1], 'l':[8.25,1], 'z':[0.75, 0], 'x':[1.75,0], 'c':[2.75,0], 'v':[3.75,0], 'b':[4.75, 0], 'n'
:[5.75, 0], 'm': [6.75, 0] }

def is_right(char):
    if(char == "y" or char=="u" or char=="i" or char=="o" or char=="p"):
        return True
    if(char == "h" or char=="j" or char=="k" or char=="l"):
        return True
    if(char == "n" or char=="m"):
        return True
    return False