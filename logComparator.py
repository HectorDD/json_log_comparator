import json

exclusionList=["sessionId","clientReferenceId"]

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

def identation(level):
    s=""
    for i in range(level):
        s+="   "
    return s

def compareLogs(json1,json2,key,level=0):
    if not isinstance(json1,dict) or isinstance(json1,list):
        if json1!=json2:
            #print("is wrong in "+ key+"."+j)
            print(identation(level)+key+": "+json1+"(WRONG)")
            return 1
        else:
            print(identation(level)+key+": "+json1)
            return 0
    for j in json1:
        if isinstance(json1[j],dict):
            try:
                compareLogs(json1[j],json2[j],key+"."+j,level+1)
            except:
                print(identation(level)+j+": "+json1[j]+"(NOT EXIST)")
                #print("the following key has problems: " + key+"."+j) 
        elif isinstance(json1[j],list):
            for i in range(len(json1[j])):
                try:
                    compareLogs(json1[j][i],json2[j][i],key+"."+j+"["+str(i)+"]",level+1)
                except:

                    print(identation(level)+j+": "+json1[j]+"(NOT EXIST)")
                    #print("the following key has problems: " + key+"."+j) 
        else:
            try:
                if json1[j] != json2[j] and not j in exclusionList:
                    #pass
                    print(identation(level)+j+": "+json1[j]+"(WRONG)")
                    #print("is wrong in "+ key+"."+j)
            except:
                print(identation(level)+j+": "+json1[j]+"(NOT EXIST)")
                #print("the following key has problems: " + key+"."+j)
        #print(identation(level)+j+": "+json1[j])
                
def compareTestCases(testCases):
    for i in testCases:
        print("CHECKING TEST CASE : "+i)
        log1=loadLog(i+"on")
        log2=loadLog(i+"off")
        print("Checking "+i+"on > "+i+"off")
        
        for j in range(len(log1)):
            print("INDEX: "+str(j))
            compareLogs(log1[j],log2[j],"global")
        print("Checking "+i+"on < "+i+"off")
        
        for j in range(len(log2)):
            print("INDEX: "+str(j))
            compareLogs(log2[j],log1[j],"global")

        
        
testCases=["logh"]

compareTestCases(testCases)
            
            
            
        