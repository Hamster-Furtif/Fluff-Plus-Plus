dc = {}
lexicon = []

libs = {}

var, const, strs, lst, mat = {}, {}, {}, {}, {}

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

a_var = alphabet
a_lst = [str(i) for i in range(1, 21)]
a_strs = [str(i) for i in range(1, 21)]
a_mat  = alphabet

group_count = {"(":0, ")":0, "{":0, "}":0, "[":0, "]":0, '"':0}
group_pairs = [('(',')'), ('{','}'), ('[',']')]
group_chars = "(){}[]"
group_left  = [e[0] for e in group_pairs]
group_right = [e[1] for e in group_pairs]

operators = "+-*/= ,"



WRITE_IN = []

def run():
    initDictionary()
    lines = readFile("samplecode")
    lines = lines[1:-1]
    i = lines.index("begin")
    begin, body = lines[:i], lines[i+1:]
    a = generateCodeInit(begin)
    for e in a:
        t = transcript(e)
        print(t)
        
def readFile(filedir, ext="fpp", clean=True):
    file = open(filedir+"."+ext, 'r', encoding="utf8")
    lines = file.read()
    if(clean):
        lines = lines.replace("\t", '')
    lines = lines.split("\n")
    return lines


def writeFile(lines, filedir, ext="fpp"):
    file = open(filedir+"."+ext,'w', encoding="utf8")
    file.writelines(lines)
    file.close()

def initDictionary():
    L = readFile("dictionary", "txt", False)
    for e in L:
        s = e.split("\t")
        try:
            dc[s[1]] = s[0]
        except IndexError:
            print("Error in dictionary: ", e)
    lexicon = list(dc.keys())

def loadLib(filedir, folder="/libs/"):
    lines = readFile(folder+filedir, ext="txt")
    funcs = []
    for i in range(len(lines)):
        line = lines[i]
        if(len(line) >= 2 and line[:2] == ">>"):
            func = []
            

def splitLine(line, split_all=False, getError=False):
    split = []
    s=0
    error = ""
    for i in range(len(line)):
        if(line[i] in operators and (checkGroups() or split_all)):
            if(s != i):
                split.append(line[s:i])
            split.append(line[i])
            if(i<len(line)-1):
                s=i+1
        elif(line[i] in group_chars):
            group_count[line[i]] += 1

    if not (line[-1] in operators):
        split.append(line[s:])        

    while(" " in split):
        split.remove(" ")
    if(getError):
        return split, error
    else:
        return split


def groupBy(split, c):
    group = [[]]
    for e in split:
        if(e != c):
            group[-1].append(e)
        else:
            group.append([])
    return group


def checkGroups():
    b = True
    for l,r in group_pairs:
        b = (b and (group_count[l] == group_count[r]))
    b = b and group_count['"']//2 == 0
    return b


def generateCodeInit(lines, detailed = False):
    global a_var, a_mat
    output = []
    for line in lines:
        split = splitLine(line)
        v = split[0]
        split = split[1:]
        
        if(v == "var"):
            groups = groupBy(split, ',')
            groups = asGoesFirst(groups)
            for g in groups:
                name = g[0]
                if(isNameAvailable(name) == True):
                    
                    if(len(g) > 2 and g[1] == "as"):                # "var gravity as G"
                        if(len(g[2]) == 1 and g[2] in a_var):
                            var[name] = g[2]
                            a_var = a_var[:a_var.index(g[2])]+a_var[a_var.index(g[2])+1:]
                            
                            if("="  not in g):
                                g = [g[0]]

                            else:                                   # "var gravity as G = 9.81"
                                g = [g[0]]+g[3:]

                    elif(len(a_var)>0):                             # "var gravity"
                        var[name] = a_var[0]
                        a_var = a_var[1:]

                    if("=" in g):                                   # "var gravity = 9.81"
                        if(g[2][0] == '{' and g[2][-1] == '}'):
                            g.insert(0, "dim")
                        g = swapAround(g)

                    if(detailed or len(g) > 1):
                        output.append(g)
                else:
                    print("Name " + name + " is already used as a variable name or as part of the language lexicon")
                    
        elif(v == "mat"):
            groups = groupBy(split, ',')
            groups = asGoesFirst(groups)
            for g in groups:
                name = g[0]
                if(isNameAvailable(name) == True):
                    if(len(g) > 2 and g[1] == "as"):                # "mat matrix as M"
                        if(len(g[2]) == 1 and g[2] in a_mat):
                            mat[name] = g[2]
                            a_mat = a_mat[:a_mat.index(g[2])]+a_mat[a_mat.index(g[2])+1:]
                            
                            if("="  not in g):
                                g = [g[0]]
                            else:                                   # "mat matrix as M = [[1, 2],[3, 4]]"
                                g = [g[0]]+g[3:]

                    elif(len(a_var)>0):                             # "mat matrix"
                        mat[name] = a_mat[0]
                        a_mat = a_mat[1:]

                    g.insert(0, "mat")
                    if("=" in g):                                   # "mat matrix = [[1, 2],[3, 4]]"
                        if(g[3][0] == '{' and g[3][-1] == '}'):
                            g.insert(0, "dim")
                        g = swapAround(g)
                    if(detailed or len(g) > 1):
                        output.append(g)
                else:
                    print("Name " + name + " is already used as a variable name or as part of the language lexicon")

        elif(v == "lst"):
            global a_lst
            groups = groupBy(split, ',')
            groups = asGoesFirst(groups)
            for g in groups:
                name = g[0]
                if(isNameAvailable(name) == True):
                    if(len(g) > 2 and g[1] == "as"):
                        if(len(g[2]) == 1 and g[2] in a_lst):
                            lst[name] = g[2]
                            a_lst = a_lst[:a_lst.index(g[2])]+a_lst[a_lst.index(g[2])+1:]

                            if("="  not in g):
                                g = [g[0]]
                            else:
                                g = [g[0]]+g[3:]

                    elif(len(a_var)>0):
                        lst[name] = a_lst[0]
                        a_lst = a_lst[1:]

                    g.insert(0, "lst")
                    if("=" in g):
                        if not(g[3][0] == '{' and g[3][-1] == '}'):
                            g.insert(0, "dim")
                        g = swapAround(g)
                    if(detailed or len(g) > 1):
                        output.append(g)
                else:
                    print("Name " + name + " is already used as a variable name or as part of the language lexicon")

        elif(v == "str"):
            global a_strs
            groups = groupBy(split, ',')
            groups = asGoesFirst(groups)
            for g in groups:
                name = g[0]
                if(isNameAvailable(name) == True):
                    if(len(g) > 2 and g[1] == "as"):                # "str s as 5"
                        if(len(g[2]) == 1 and g[2] in a_strs):
                            strs[name] = g[2]
                            a_strs = a_strs[:a_strs.index(g[2])]+a_strs[a_strs.index(g[2])+1:]

                            if("="  not in g):
                                g = [g[0]]
                            else:                                   # "str  s as 5 = "Hello World""
                                g = [g[0]]+g[3:]

                    elif(len(a_var)>0):                             # "str s"
                        strs[name] = a_strs[0]
                        a_strs = a_strs[1:]

                    g.insert(0, "str")
                    if("=" in g):                                   # "str s = "Hello World""
                        g = swapAround(g)
                    if(detailed or len(g) > 1):
                        output.append(g)
                else:
                    print("Name " + name + " is already used as a variable name or as part of the language lexicon")

        elif(v == "const"):                          #constants always look like "const G = 9.81"
            groups = groupBy(split, ',')
            for g in groups:
                if(len(g) == 3):
                    name = g[0]
                    if(isNameAvailable(name) == True):
                        const[g[0]] = g[2]        

        else:
            print("Failed", split)

    return output

def generateMainCode(lines):
    output = []
    for l in lines:
        split = splitLine(l)
        split = replaceLogical(split)
        if split[0] == "for":
            i = split.index("to")
            split[1:i] = swapAround(split[1:i])
        
            
            

        

def asGoesFirst(groups): #put the groups containing "as" at the top of the queue
    temp = []
    for g in groups:
        if("as" in g):
            temp.insert(0, g)
        else:
            temp.append(g)
    return temp
            
            

def isNameAvailable(name):
    for l in [var, const, strs, lst, mat, dc]:
        if (name in list(l.keys())):
            return l
    return True

def swapAround(split, c="="):
    if(c in split):
        return split[split.index(c)+1:] + [c] + split[:split.index(c)]
    else:
        return "ERROR: Swap error, string not found: no occurence of '" + c + "' in '" + str(split) + "'" 



def transcript(split):
    if(len(split) > 1):
        left = transcript([split[0]])
        right = transcript(split[1:])
        try:
            return left+right
        except TypeError:
            print("Failed to assemble transcript ", left, "with", right)
    elif(len(split) == 1):
        elem = split[0]
        L = isNameAvailable(elem)
        if(L != True):           #Is it a stored variable ?
            return L[elem]
        
        elif(elem.isdigit()):    #Is it an integer ?
            return elem

        elif(isFloat(elem)):     #Is it a float ?
            return elem

        elif(elem[0] in group_chars and elem[-1] in group_chars):  #transcripts {},[] and () blocks
            local_split = splitLine(elem[1:-1])
            total = elem[0]
            for e in split:
                total += transcript(local_split)
            total += elem[-1]
            return total

        elif(elem[0] == '"' and elem[-1] == '"'): #searches for custom chars
            s=1
            for i in range(1, len(elem)-2):
                if(elem[i] == '$' and elem[i-1] != "\\"):
                    s=i+1
                    for j in range(i+1, len(elem)-1):
                        if(elem[j] == '$' and elem[j-1] != "\\"):
                            elem = elem[:s-1] + dc[elem[s:j]] + elem[j+1:]
                            i = 2
                            break
            return elem
        elif(elem in lexicon):   #Is it part of the lexicon ?
            return dc[elem]
        
        else:
            print("No match for: ", elem)
    else:
        print("Split is empty !")



def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def replaceLogical(split):
    i = 1
    for i in range(1, len(split)):
        if(split[i] == "=" and split[i-1] in "=!><"):
            split[i-1] += "="
            split[i] = ""
    while("" in split):
        split.remove("")
    return split

def test(s):
    initDictionary()
    a = generateCodeInit([s])
    for e in a:
        print(transcript(e))
