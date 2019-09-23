import requests
from requests.auth import HTTPBasicAuth
from logComparator import *


pamDBUrl="http://localhost:8090/api/pam/sessionData?sessionId="

def getSession(sessionId):
	response = requests.get(pamDBUrl+sessionId)
	return response.json()

def compareSessions(sessionId1,sessionId2):
	session1=getSession(sessionId1)
	print("session1 : "+sessionId1)
	print(session1)
	session2=getSession(sessionId2)
	print("session2 : "+sessionId2)
	print(session2)
	print("Comparing session1 > session2")
	compareLogs(session1,session2,"global")
	print("Comparing session1 < session2")
	compareLogs(session2,session1,"global")


#compareSessions("8dabbae4-94de-4dce-bfa0-747a8995de52","6a2dea9a-1ab1-4894-a413-7e4603bbc89b")
compareSessions("e5db7cbd-8b65-41cf-b55b-e546f135468c","611d3b49-ad1e-452e-8509-4ec0dec2837d")
