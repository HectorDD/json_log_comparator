import json

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

def compareLogs(json1,json2,key):
    for j in json1:
        if isinstance(json1[j],dict):
            compareLogs(json1[j],json2[j],key+"."+j)
        elif isinstance(json1[j],list):
            for i in range(len(json1[j])):
                compareLogs(json1[j][i],json2[j][i],key+"."+j+"["+str(i)+"]")
        else:
            if json1[j] == json2[j]:
                #pass
                #print(j + " is OK in " + key+j)
                pass
            else:
                print("is wrong in "+ key+"."+j)
                
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
        
        
        
                
            

TestCases=["test1"]

compareTestCases(TestCases)
            
            
            
        