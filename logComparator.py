import json
import os
import webbrowser

exclusionList=["sessionId","clientReferenceId"]

def identation(level):
    s=""
    for i in range(level):
        s+="&nbsp;&nbsp;&nbsp;&nbsp;"
    return s

def printLine(s,conflicts,key):
    if key in conflicts["wrong"]:
        return "<b><div style='color:red'>"+s+" [WRONG]</div></b>"
    elif key in conflicts["nonexits"]:
        return "<b><div style='color:orange'>"+s+" [NONEXISTS]</div></b>"
    else:
        return "<div>"+s+"</div>"

def generateHTML(jsonFile1,jsonFile2):
    f = open('holamundo.html','w')
    conflicts1=compareLogs(jsonFile1,jsonFile2)
    conflicts2=compareLogs(jsonFile2,jsonFile1)
    content="<html><header><style>#global {height: 800px;border: 1px solid #ddd;background: #f1f1f1;overflow-y: scroll;}table {border: 1px solid DarkOrange;border-radius: 13px; border-spacing: 0;}</style></header><body><center><h2>JSON Comparator Report</h2></center><br><center><table border='1' width=90% cellpadding='10'><tr><td valign='top'>"
    content+="<div id='global'>"
    content+=printJson(jsonFile1,conflicts1)
    content+="</div></td><td><div id='global'>"
    content+=printJson(jsonFile2,conflicts2)
    content+="</div></td></tr></table></body></html>"
    f.write(content)
    url='file://' +os.path.realpath(f.name)
    f.close()
    print("HTML Report in:",url)
    webbrowser.open(url,new=2)


def printJson(jsonFile,conflicts,key=None,result=""):
    if key==None:
        key=[]
    if not isinstance(jsonFile,str):
        for i in jsonFile:
            if isinstance(jsonFile[i],dict):
                s=identation(len(key))+i+": "
                result+=printLine(s,conflicts,key+[i])+"<br>"
                result+=printJson(jsonFile[i],conflicts,key+[i])
            elif isinstance(jsonFile[i],list):
                s=identation(len(key))+i+": "
                result+=printLine(s,conflicts,key+[i])+"<br>"
                for j in jsonFile[i]:
                    result+=printJson(j,conflicts,key+[i])
            else:
                s=identation(len(key))+i+": "+str(jsonFile[i])
                result+=printLine(s,conflicts,key+[i])+"<br>"
    return result
            

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
            conflicts["wrong"].append(key)
            print("is wrong in ",key)
            return 1
        else:
            return 0
    for j in json1:
        if isinstance(json1[j],dict):
            try:
                compareLogs(json1[j],json2[j],key+[j],conflicts)
            except:
                conflicts["nonexits"].append(key+[j])
                #print("the following key has problems: ", key+[j]) 
        elif isinstance(json1[j],list):
            for i in range(len(json1[j])):
                try:
                    compareLogs(json1[j][i],json2[j][i],key+[j],conflicts)
                except:
                    conflicts["nonexits"].append(key+[j])
                    #print("the following key has problems: ",key+[j]) 
        else:
            try:
                if json1[j] != json2[j] and not j in exclusionList:
                    conflicts["wrong"].append(key+[j])
                    #print("is wrong in ",key+[j])
            except:
                conflicts["nonexits"].append(key+[j])
                #print("the following key has problems: ",key+[j])
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
            print(printJson(log1[j],conflicts))
        print("Checking "+i+"on < "+i+"off")
        
        for j in range(len(log2)):
            print("INDEX: "+str(j))
            conflicts=compareLogs(log2[j],log1[j])
            print(printJson(log2[j],conflicts))

        
testCases=["logh"]

#compareTestCases(testCases)
#log1=loadLog("loghon")[0]
#log2=loadLog("loghoff")[0]
#generateHTML(log1,log2)

            
            
            
        