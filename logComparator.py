import json

exclusionList=["sessionId","clientReferenceId"]

def identation(level):
    s=""
    for i in range(level):
        s+="   "
    return s

def printLine(s,conflicts,key):
    if key in conflicts["wrong"]:
        print(s+" [WRONG]")
    elif key in conflicts["nonexits"]:
        print(s+" [NONEXISTS]")
    else:
        print(s)

def generateHTML(jsonFile,conflicts,key=None):
    f = open('holamundo.html','w')
    content="<html><header></header><body><table width=100%><tr><td>"

    content+="</td><td>"

    content+="</td></tr></table></body></html>"


def printJson(jsonFile,conflicts,key=None):
    if key==None:
        key=[]
    for i in jsonFile:
        if isinstance(jsonFile[i],dict):
            s=identation(len(key))+i+": "
            printLine(s,conflicts,key+[i])
            printJson(jsonFile[i],conflicts,key+[i])
        elif isinstance(jsonFile[i],list):
            s=identation(len(key))+i+": "
            printLine(s,conflicts,key+[i])
            for j in jsonFile[i]:
                printJson(j,conflicts,key+[i])
        else:
            s=identation(len(key))+i+": "+str(jsonFile[i])
            printLine(s,conflicts,key+[i])
            

def extractJson(file):
    listOfLines=file.readlines()
    counter=0
    listOfJson=[]
    temp=""
    for i in listOfLines:
        if counter!=0:
            temp+=i
        if "{" in i:
            if counter==0:
                temp+=i
            counter+=1
        if "}" in i:
            counter=counter-1
            if counter==0:
                #temp = temp.replace("'", "\"")
                dictionary = json.loads(temp)
                listOfJson.append(dictionary)
                temp=""
    return listOfJson
    
def loadLog(name):
    f=open(name,"r")
    listOfJson=extractJson(f)
    return listOfJson

def compareLogs(json1,json2,key=None,conflicts=None):
    if conflicts==None:
        conflicts={"wrong":[],"nonexits":[]}
    if key==None:
        key=[]
    if not isinstance(json1,dict) or isinstance(json1,list):
        if json1!=json2:
            conflicts["wrong"].append(key+[j])
            print("is wrong in ",key+[j])
            return 1
        else:
            return 0
    for j in json1:
        if isinstance(json1[j],dict):
            try:
                compareLogs(json1[j],json2[j],key+[j],conflicts)
            except:
                conflicts["nonexits"].append(key+[j])
                print("the following key has problems: ", key+[j]) 
        elif isinstance(json1[j],list):
            for i in range(len(json1[j])):
                try:
                    compareLogs(json1[j][i],json2[j][i],key+[j],conflicts)
                except:
                    conflicts["nonexits"].append(key+[j])
                    print("the following key has problems: ",key+[j]) 
        else:
            try:
                if json1[j] != json2[j] and not j in exclusionList:
                    conflicts["wrong"].append(key+[j])
                    print("is wrong in ",key+[j])
            except:
                conflicts["nonexits"].append(key+[j])
                print("the following key has problems: ",key+[j])
    return conflicts
                
def compareTestCases(testCases):
    for i in testCases:
        print("CHECKING TEST CASE : "+i)
        log1=loadLog(i+"on")
        log2=loadLog(i+"off")
        print("Checking "+i+"on > "+i+"off")
        
        for j in range(len(log1)):
            print("INDEX: "+str(j))
            conflicts=compareLogs(log1[j],log2[j])
            printJson(log1[j],conflicts)
        print("Checking "+i+"on < "+i+"off")
        
        for j in range(len(log2)):
            print("INDEX: "+str(j))
            conflicts=compareLogs(log2[j],log1[j])
            printJson(log2[j],conflicts)
        
        
testCases=["logh"]

compareTestCases(testCases)
            
            
            
        