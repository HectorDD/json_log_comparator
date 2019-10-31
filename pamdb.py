import requests
from requests.auth import HTTPBasicAuth
from logComparator import *


pamDBUrl="http://localhost:8090/api/pam/sessionData?sessionId="

def getSession(sessionId):
	response = requests.get(pamDBUrl+sessionId)
	return response.json()


def compareSessions(sessionId1,sessionId2):
	session1=getSession(sessionId1)
	session2=getSession(sessionId2)
	generateHTML(session1,session2)


#compareSessions("8dabbae4-94de-4dce-bfa0-747a8995de52","6a2dea9a-1ab1-4894-a413-7e4603bbc89b")
compareSessions("f14e6eac-8853-494a-b981-d7a294d3219a","ad9e5eb1-9481-4967-abbd-68bcb2df213e")
