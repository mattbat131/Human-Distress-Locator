import subprocess
import os
import pycurl
from io import BytesIO
import json

num = input('How many tags? ')
tag = list()
for i in range(int(num)):
	n = input("Tag: ")
	tag.append(n)
key = input('Enter Key: ')

#file = input('JSON File: ')

def runCommand():
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(command)	

def curl(u):
    buffer = BytesIO()
    c = pycurl.Curl()
    curl = u
    c.setopt(pycurl.URL, curl)
    c.setopt(pycurl.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue()
    return body.decode('iso-8859-1')

def getId():
    id = list()
    for j in range(int(num)):
   	 id += [i['id'] for i in json_result[j]['results']]
    return id

def exists(idList, testId):
   for i in idList:
       if i == testId:
           return True
   return False
 
def createARFF():
	f = open("HumanDistress.arff".format(i), 'w')
	f.write("@RELATION sounds\n @ATTRIBUTE class\t {Human-In-Distress, Other}\n @DATA\n")
	for jF in id_result:
		if "human" in jF["tags"] and ("distress" in jF["tags"] or "crying" in jF["tags"]    or "pain" in jF["tags"] or "screaming" in jF["tags"] or "moaning" in jF["tags"] or "scared" in jF["tags"] or "yelling" in jF["tags"]):
			#write to file under Human-In-Distress
			f.write("stuff")
		else:
			#write to file under Other
			f.write("stuff")


#Gets .json file of all sounds with same tags
json_result = list()
for i in range(int(num)):
	url = 'http://www.freesound.org/apiv2/search/text/?query={0}&token={1}'.format(tag[i], key)
	json_result.append(json.loads(curl(url), encoding ='iso-8859-1'))

#Gets id's of all sounds from tag searches	
allId = getId()

#Gets all .json files from ids
blackListId = list()
id_result = list()
for i in allId:
	if exists(blackListId, i) == False:
		url = 'https://www.freesound.org/apiv2/sounds/{0}'.format(i)
		id_result.append((json.loads(curl(url), encoding='iso-8859-1')))
	blackListId.append(i)

print(id_result)
#Creates .ARFF file
createARFF()
