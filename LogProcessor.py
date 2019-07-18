# coding = utf-8
##############################
## Install xmltodict
## pip3.7 install xmltodict
##############################
import xmltodict
import json
import sys
import re
from logComparator import *

def cleanKey(key):
    index=key.find(':')
    if index!=-1:
        key=key[index+1:]
    return key

def cleanDict(dictionary):
    if not isinstance(dictionary,dict) or isinstance(dictionary,list):
        return dictionary
    result={}
    for j in dictionary:
        if j == "#text":
            return dictionary[j]
        elif not "@xmlns" in j:
            key=cleanKey(j)
            if isinstance(dictionary[j],dict):
                result[key]=cleanDict(dictionary[j])
            elif isinstance(dictionary[j],list):
                temp=[]
                for i in dictionary[j]:
                    temp.append(cleanDict(i))
                result[key]=temp
            else:
                result[key]=dictionary[j]
    return result

class LogProcess:

    def __init__(self, fileName, invalidTags,outputName):
        self.fileName = fileName
        self.invalidTags = invalidTags
        self.outputFile = open(outputName,"w")

    def process():
        return "Hi my friend"

    def isValidTag(self, vtag):
        # print( self.invalidTags )
        for invalidTag in self.invalidTags:
            if invalidTag in vtag :
                return False
        return True


    def parseToJson(self, currentXML):

        #print("\n====================parseToJson================")
        try:
            # print("===============================================")
            # print("***********************************************")
            # print("====================XML========================")
            # print( currentXML)
            jsonVal = cleanDict(xmltodict.parse(currentXML))
            # print("********************JSON***************************")
            print(jsonVal)
            self.outputFile.write("===============================================\n")
            self.outputFile.write(str(jsonVal)+"\n")
            self.outputFile.write("===============================================\n")
            print("===============================================")
            # print("***********************************************")
            # print("===============================================")
        except:
            print("Oops!",sys.exc_info()[0],"occured.")
            print("Next entry.")
            print()

    def process(self):
        logFile=open(self.fileName, "r")
        lines=logFile.readlines()
        currToken=""
        currentXML=""
        tokens=[]
        readingToken=False
        prevChar=''
        isXMLReading=False
        nsPattern="xmlns:.*[^\s]+[^>]"

        for line in lines:
            for c in line:
                if isXMLReading :
                    currentXML = currentXML + c
                if c == '>' :
                    popped=False
                    if len(tokens) > 0 :
                        if currToken == tokens[-1]:
                            #print("POP: " + currToken)
                            tokens.pop()
                            popped=True
                            if isXMLReading and len(tokens) == 0 :
                                self.parseToJson(currentXML)
                                currentXML=""
                                tokens=[]
                                isXMLReading=False

                    if(not popped and prevChar!='/'
                        and len(currToken.strip()) > 0
                        and self.isValidTag(currToken)) :
                        #print("PUSH: " + currToken)
                        tokens.append(currToken.strip())
                        if not isXMLReading:
                            # First token
                            currentXML = "<"+currToken+">"
                            isXMLReading=True
                    currToken=""
                if c == '<':
                    readingToken=True
                if c=='>' or c==' ':
                    readingToken=False
                elif readingToken:
                    if c!= '<' and c!='/':
                        currToken=currToken + c
                prevChar=c

def convertXMLtoJson(inputName,outputName):
    fstrip = lambda x:x.strip()
    invalidTags = [fstrip(x) for x in open("invalid-tags.txt", "r").readlines()]
    logProcess = LogProcess(inputName, invalidTags,outputName)
    logProcess.process()
    logProcess.outputFile.close()

fileName="XMLRequests_ToggleOFF_ECC_ICCR.xml" # "test_1.xml" #
#fileName="$WORKDIR/Docker/logs/esb-server/mule-app-CC-ESB-CreditCheckVZW-2.0.log"
convertXMLtoJson(fileName,"someOutput")
#print( tokens)
