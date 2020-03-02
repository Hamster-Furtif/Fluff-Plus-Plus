dc = {}
lexicon = []

libs = {}

var, const, strs, lst, mat = {}, {}, {}, {}, {}

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

a_var = alphabet
a_lst = [str(i) for i in range(1, 21)]
a_strs = [str(i) for i in range(1, 21)]
a_mat  = alphabet

group_chars = '(){}[]'

operators = '+-*/= ,<>'

LINE_END = "Ù"

def run(name, path="", r=True):
    if r:
        reset()
    WRITE_IN = ["Filename:"+name+"\n"]
    loadLib("math", is_default_lib = True)
    loadLib("utils", is_default_lib = True)
    loadLib("casioIO", is_default_lib = True)
    initDictionary()
    lines = readFile(path+name)
    lines = lines[1:lines.index("end")]
    while("" in lines):
        lines.remove("")
    i = lines.index("begin")
    begin, body = lines[:i], lines[i+1:]
    a = generateCodeInit(begin)
    for e in a:
        t = transcript(e, "Transcript code init")
        print(t)
        WRITE_IN.append(t+LINE_END)
    for l in body:
        e = generateMainCode(l)
        t = transcript(e, "Transcript main code")
        print(t)
        WRITE_IN.append(t+LINE_END)
    DEF = []
    for i in range(len(WRITE_IN)):
        line = WRITE_IN[i]
        L = len(line)
        n = L//256
        for i in range(n+1):
            DEF.append(line[256*i:min(256*(i+1), L)]+"\n")
            
    writeFile(DEF, path+name)
        
def readFile(filedir, ext="fpp", clean=True):
    file = open(filedir+"."+ext, 'r', encoding="utf8")
    lines = file.read()
    if(clean):
        lines = lines.replace("\t", '')
    lines = lines.split("\n")
    return lines

def reset():
    dc = {}
    lexicon = []
    libs = {}
    var, const, strs, lst, mat = {}, {}, {}, {}, {}
    a_var = alphabet
    a_lst = [str(i) for i in range(1, 21)]
    a_strs = [str(i) for i in range(1, 21)]
    a_mat  = alphabet
    group_count = {"(":0, ")":0, "{":0, "}":0, "[":0, "]":0, '"':0}

def writeFile(lines, filedir, ext="cfp"):
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

def loadLib(filedir, folder="libs/", is_default_lib=False):
    lines = readFile(folder+filedir, ext="txt")
    libname = ""
    if not is_default_lib:
        libname = lines[0]+"."
    for i in range(1, len(lines)):
        line = lines[i]
        if(len(line) >= 2 and line[:2] == ">>"):
            line = line[2:]
            body = ""
            while lines[i+1] != "<<":
                i += 1
                body += lines[i]+"\n"
            body = body[:-1]
            libs[libname+line] = body
            
def findFromLibs(string):
    if(string.startswith("menu(")):
        args = string[string.index('('):]
        return "Menu " + transcript([args], "Special case menu in findFromLibs")[1:-1]
    if(string.startswith("absolute(")):
        L = isNameAvailable(string[string.index('(')+1:-1])
        if(L != True):
            return str(L[string[string.index('(')+1:-1]])
        
    if('(' in string):
        keys = list(libs.keys())
        pattern = string[0:string.index('(')]
        
        args = string[string.index('(')+1:-1]
        groups = []

        
        if args != "":
            args = splitLine(args)
            groups = groupBy(args, ",")

        args = []
        for g in groups:
            total = ""
            for e in g:
                total += transcript([e], "Transcript findFromLibs")
            args.append(total)
            
        for k in keys:
            if k[0:k.index('(')] == pattern:
                params = k[k.index('(')+1:-1]
                if params == "":
                    return libs[k]

                params = splitLine(params, ops=", ")
                while ',' in params:
                    params.remove(',')
                    
                result = libs[k]
                for i in range(len(args)):
                    result = result.replace(params[i], args[i])
                return result
    return False

def splitLine(line, ops=operators):
    group_count = {"(":0, ")":0, "{":0, "}":0, "[":0, "]":0, '"':0}
    split = []
    error = ""
    in_string = False
    sz = len(line)
    s=0
    for i in range(sz):
        
        if(line[i] == '"'):
            in_string = not in_string
            
        if not in_string:
            c = line[i]
            
            if c in ops and checkGroups(group_count):
                if(s != i):
                    split.append(line[s:i])
                split.append(line[i])
                if(i<len(line)-1):
                    s=i+1
                    
            elif c in group_chars:
                group_count[c] += 1
                if(checkGroups(group_count)):
                    split.append(line[s:i+1])
                    s=i+1
                elif (c == "[" and line[i-1] != "]" and line[i-1] != "[" and group_count['('] == group_count[')'] and group_count['['] == group_count[']']+1):
                    split.append(line[s:i])
                    s=i
                    
    if not (line[-1] in operators):
        split.append(line[s:])        

    while(" " in split):
        split.remove(" ")
        
    split = replaceLogical(split)
    return split

            
def groupBy(split, c):
    group = [[]]
    for e in split:
        if(e != c):
            group[-1].append(e)
        else:
            group.append([])
    return group


def checkGroups(group_count):
    b = True
    for i in range(0, len(group_chars), 2):
        l = group_chars[i]
        r = group_chars[i+1]
        b = (b and (group_count[l] == group_count[r]))
    return b

def groupCountTotal(group_count):
    s = 0
    for e in group_chars:
        s += group_count[e]
    return s


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

                    if("=" in g):                                   # "mat matrix = [[1, 2],[3, 4]]"
                        if(g[2][0] == '{' and g[2][-1] == '}'):
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

                    if("=" in g):
                        if not (g[2][0] == '{' and g[2][-1] == '}' or g[2] in list(lst.keys())) :
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

        elif(v == "import"):
            groups = groupBy(split, ',')
            for g in groups:
                loadLib(g[0])

        else:
            print("Failed", split)

    return output

def generateMainCode(line):
    split = splitLine(line)
    split = replaceLogical(split)
    if split[0] == "for":
        i = split.index("to")
        split[1:i] = swapAround(split[1:i])
    elif "causes" in split and "=" in split:
        i = split.index("causes")
        split[i+1:] = swapAround(split[i+1:])
    elif "=" in split:
        split = swapAround(split)
    return split
            
            

        

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
        print("ERROR: Swap error, string not found: no occurence of '" + c + "' in '" + str(split) + "'" )



def transcript(split, origin="(Origin Unknown)"):

    if(type(split) != list):
        print("Warning in transcript from '" + origin + "' ! list expected, instead found ", type(split), ". Autocorrection may cause further issues.")
        split = [split]
        
    if(len(split) > 1 ):
        left = transcript([split[0]], "left")
        right = transcript(split[1:], "right")
        try:
            return left+right
        except TypeError:
            print("Failed to assemble transcript ", left, "with", right)
    elif(len(split) == 1):
        elem = split[0]
        L = isNameAvailable(elem)
        INLIBS = findFromLibs(elem)
        
        if(L != True):           #Is it a stored variable ?
            return getPrefix(L) + L[elem]
                
        elif(elem.isdigit()):    #Is it an integer ?
            return elem

        elif(isFloat(elem)):     #Is it a float ?
            return elem

        elif(elem[0] in group_chars and elem[-1] in group_chars):  #transcripts {},[] and () blocks
            local_split = splitLine(elem[1:-1])
            total = elem[0]
            total += transcript(local_split, 3)
            total += elem[-1]
            return total

        elif(elem[0] == '"' and elem[-1] == '"'): #searches for custom chars
            n = (elem.count("$")-elem.count("\\$"))/2
            n = int(n)
            for i in range(n):
                k = elem.index("$")
                while (elem[k-1] == "\\"):
                    k = elem.index("$", k+1)
                l = elem.index("$", k+1)
                elem = elem.replace(elem[k:l+1], dc[elem[k+1:l]], 1)
            return elem

        elif(elem in lexicon):   #Is it part of the lexicon ?
            return dc[elem]

        elif(INLIBS):            #Is it from a lib ?
            return INLIBS
        elif('[' in elem and False):
            k = elem.index('[')
            return transcript([elem[:k],elem[k:]])
        
        else:
            print("ERROR: No match for: '"+elem+"'")
            return ">"+elem+"<"
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


def getPrefix(L):
    if(L == mat):
        return "Mat "
    elif(L == lst):
        return "List "
    elif(L == strs):
        return "Str "
    else:
        return ""
