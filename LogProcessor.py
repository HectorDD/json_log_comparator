# coding = utf-8
##############################
## Install xmltodict
## pip3.7 install xmltodict
##############################
import xmltodict
import json
import sys
import re

class LogProcess:

    def __init__(self, fileName, invalidTags):
        self.fileName = fileName
        self.invalidTags = invalidTags

    def process():
        return "Hi my friend"

    def isValidTag(self, vtag):
        # print( self.invalidTags )
        for invalidTag in self.invalidTags:
            if invalidTag in vtag :
                return False
        return True

    def parseToJson(self, currentXML):

        print("\n====================parseToJson================")
        try:
            print("===============================================")
            print("***********************************************")
            print("====================XML========================")
            print( currentXML)
            jsonVal = json.loads(json.dumps(xmltodict.parse(currentXML)))
            print("********************JSON***************************")
            print(jsonVal)
            print("===============================================")
            print("***********************************************")
            print("===============================================")
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



fileName="/Users/aldemar/Documents/work/cci/Docker/logs/pam-proxy/membrane-proxy.log" # "test_1.xml" #
#fileName="$WORKDIR/Docker/logs/esb-server/mule-app-CC-ESB-CreditCheckVZW-2.0.log"
fstrip = lambda x:x.strip()
invalidTags = [fstrip(x) for x in open("invalid-tags.txt", "r").readlines()]
logProcess = LogProcess(fileName, invalidTags)
logProcess.process()
#print( tokens)
