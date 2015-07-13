import datetime
from io import BytesIO
import json
import os
import pycurl
import subprocess

API_KEY_FILE = "ApiKey.txt"
OUTPUT_FILE = "HumanDistress.arff"
SEARCH_FOR_TAG_URL = 'http://www.freesound.org/apiv2/search/text/?query={0}&token={1}'
URL_FOR_ONE_ID = 'http://www.freesound.org/apiv2/sounds/{0}/?token={1}'
FILE_ATTRIBUTES = ["bitrate", "bitdepth", "duration"]
SIMPLE_STATS = ["min", "max", "mean"]
FULL_STATS = ["min", "max", "dvar2", "dmean2", "dmean", "var", "dvar", "mean"]
LOW_LEVEL_WITH_FULL_STATS = ["spectral_complexity", "silence_rate_20dB", "spectral_rms", "spectral_kurtosis", "barkbands_kurtosis",
                            "spectral_spread", "pitch", "dissonance", "spectral_energyband_high", "spectral_flux", "silence_rate_30dB",
                            "spectral_energyband_middle_high", "barkbands_spread", "spectral_centroid", "pitch_salience",
                            "silence_rate_60dB", "spectral_entropy", "spectral_rolloff", "spectral_energyband_low", "barkbands_skewness",
                            "pitch_instantaneous_confidence", "spectral_energyband_middle_low", "spectral_strongpeak", "spectral_energy",
                             "spectral_flatness_db", "zerocrossingrate", "spectral_skewness", "hfc", "spectral_crest"]
LOW_LEVEL = ["average_loudness"]

SFX = ["pitch_min_to_total", "tc_to_total", "pitch_max_to_total", "max_to_total", "duration", "pitch_after_max_to_before_max_energy_ratio"]
SFX_WITH_SIMPLE_STATS = ["temporal_decrease", "der_av_after_max", "temporal_spread", "temporal_kurtosis", "logattacktime", "temporal_centroid",
                            "flatness", "max_der_before_max", "pitch_centroid", "temporal_skewness", "effective_duration", ]
SFX_WITH_FULL_STATS = ["inharmonicity", "strongdecay", "oddtoevenharmonicenergyratio"]
# potentially add: scvalleys


def getUserInput():
    userInput = dict()
    num = input('How many tags? ')
    userInput['numberOfTags'] = num
    tags = list()
    for i in range(int(num)):
        n = input("Tag: ")
        tags.append(n)
    userInput["tags"] = tags
    key = ""
    try:
        key_file = open(API_KEY_FILE, 'r')
        key = key_file.readline().strip()
    except:
        key = input('Enter Key: ')
    userInput["key"] = key
    return userInput

def runCommand():
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(command)	

def curl(url):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue()
    return body.decode('iso-8859-1')

def getIdsFromTagResult(tagResult):
    return [result['id'] for result in tagResult['results']]

def getJsonFromUrl(url):
    curl_result = curl(url)
    json_result = json.loads(curl_result, encoding='iso-8859-1')
    return json_result

def getAllJsonResultsFromIds(ids, key):
    dedupe_list = list()
    id_result = list()
    for i in ids:
        if not i in dedupe_list:
            url = URL_FOR_ONE_ID.format(i, key)
            id_result.append(getJsonFromUrl(url))
        dedupe_list.append(i)
    return (id_result)

def createOneAttributeLine(name):
    return "@ATTRIBUTE " + name + " NUMERIC\n"

def expandStats(name, stats, prefix=""):
    full_attribute_names = [prefix + name + "_" + stat for stat in stats]
    return full_attribute_names

def getAllAttributes():
    allAttributes = list()
    allAttributes.extend(FILE_ATTRIBUTES)
    allAttributes.extend(["low_level_" + name for name in LOW_LEVEL])
    allAttributes.extend([expandStats(name, FULL_STATS, "low_level_") for name in LOW_LEVEL_WITH_FULL_STATS])
    allAttributes.extend(["sfx_" + name for name in SFX])
    allAttributes.extend([expandStats(name, SIMPLE_STATS, "sfx_") for name in SFX_WITH_SIMPLE_STATS])
    allAttributes.extend([expandStats(name, FULL_STATS, "sfx_") for name in SFX_WITH_FULL_STATS])
    return allAttributes
 
def writeHeader(filename):
    f = open(filename, 'w')
    f.write("% " + str(datetime.datetime.now()) + "\n")
    f.write("@RELATION sounds\n\n")
    allAttributes = getAllAttributes()
    for i in range(len(allAttributes)):
        for attrib in allAttributes[i]:
            print(attrib)
            f.writelines(createOneAttributeLine(attrib))
    f.write("@ATTRIBUTE class {Human-In-Distress, Other}\n\n")
    f.write("@DATA\n")

def createArff(filename, jsonFiles):
    writeHeader(filename)
    f = open(filename, 'aw')
    for jF in jsonFiles:
      f.write("{0},{1},{2},".format(jF['bitrate'], jF['bitdepth'], jF['duration']))
      analysis = json.loads(curl(jF['analysis_stats']), encoding='iso-8859-1')
      #f.write("{0},{1}".format())
      if "human" in jF["tags"] and ("distress" in jF["tags"] or "crying" in jF["tags"]    or "pain" in jF["tags"] or "screaming" in jF["tags"] or "moaning" in jF["tags"] or "scared" in jF["tags"] or "yelling" in jF["tags"]):
     		#write to file under Human-In-Distress
     		f.write("Human-In-Distress\n")
      else:
     		#write to file under Other
     		f.write("Other\n")
      #f.write("% {0}: {1} {2} %".format(jF["id"], jF["name"], jF["tags"].join(, )))

#Gets .json file of all sounds with same tags
def main():
    userInput = getUserInput()
    allIds = list()
    for tag in userInput["tags"]:
        url = SEARCH_FOR_TAG_URL.format(tag, userInput['key'])
        json_result = getJsonFromUrl(url)
        allIds.append(getIdsFromTagResult(json_result))
    allJsonForIds = list()
    for id in allIds:
        allJsonForIds = getAllJsonResultsFromIds(id, userInput['key']) 

    createArff(OUTPUT_FILE,  allJsonForIds)

if __name__ == "__main__":
    main()
