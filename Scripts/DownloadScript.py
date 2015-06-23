import subprocess
import os
import pycurl
from io import BytesIO
import json

tag = input('Enter Tag: ')
key = input('Enter Key: ')
file = input('JSON File: ')

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
    return body

def getId():
    id = [i['id'] for i in json_result['results']]
    return id

def createJson(ids, u):
    for i in ids:
        buffer = BytesIO()
        body = curl(u)
        f = open("{0}.json".format(i), 'w')
        f.write(
    
#Creates .json file of all sounds with same singular tag
url = 'http://www.freesound.org/apiv2/search/text/?query={0}&token={1}'.format(tag, key)
json = curl(url)


#Gets id's of all sounds from .json
json_result = json.loads(body.decode('iso-8859-1'))
allId = getId()

#Gets .json for each sound 
url = 'https://www.freesound.org/apiv2/sounds/{0}/analysis/?token={1}'.format(i, key)
createJson(allId, url)    

#Create .aarf file
#convertJsonToAarf()

#f = open("{0}.json".format(i), 'w')
#f.write(idInfo.decode('iso-8859-1'))
