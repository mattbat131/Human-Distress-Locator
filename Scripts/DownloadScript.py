import datetime
from io import BytesIO
import json
import pycurl


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

SFX = ["pitch_min_to_total", "tc_to_total", "pitch_max_to_total", "max_to_total", "duration", "pitch_after_max_to_before_max_energy_ratio", "strongdecay"]
SFX_WITH_SIMPLE_STATS = ["temporal_decrease", "der_av_after_max", "temporal_spread", "temporal_kurtosis", "logattacktime", "temporal_centroid",
                            "flatness", "max_der_before_max", "pitch_centroid", "temporal_skewness", "effective_duration", ]
SFX_WITH_FULL_STATS = ["inharmonicity", "oddtoevenharmonicenergyratio"]
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

def createOneAttributeLine(attribute):
    return "@ATTRIBUTE " + '_'.join(attribute) + " NUMERIC\n"

def expandStats(category, name, stats):
    attributes = [[category, name, stat] for stat in stats]
    return attributes

def getAllAttributes():
    allAttributes = list()
    #allAttributes.extend([[attrib] for attrib in FILE_ATTRIBUTES]) File attributes are in a different json object TODO
    allAttributes.extend([["lowlevel", name] for name in LOW_LEVEL])
    for name in LOW_LEVEL_WITH_FULL_STATS:
        allAttributes.extend(expandStats("lowlevel", name, FULL_STATS))
    allAttributes.extend([["sfx", name] for name in SFX])
    for name in SFX_WITH_SIMPLE_STATS:
        allAttributes.extend(expandStats("sfx", name, SIMPLE_STATS))
    for name in SFX_WITH_FULL_STATS:
        allAttributes.extend(expandStats("sfx", name, FULL_STATS))
    return allAttributes
 
def writeHeader(file, allAttributes):
    file.write("% " + str(datetime.datetime.now()) + "\n")
    file.write("@RELATION sounds\n\n")
    for attrib in allAttributes:
        file.write(createOneAttributeLine(attrib))
    file.write("@ATTRIBUTE bitrate NUMERIC\n")
    file.write("@ATTRIBUTE bitdepth NUMERIC\n")
    file.write("@ATTRIBUTE duration NUMERIC\n")
    file.write("@ATTRIBUTE class {Human-In-Distress, Other}\n\n")
    file.write("@DATA\n")

def findAttributeValue(jsonObject, attribute):
    for tag in attribute[0:-1]:
        if tag in jsonObject:
            jsonObject = jsonObject[tag]
    value = "?"
    if (attribute[-1] in jsonObject):
        potential_value = str(jsonObject[attribute[-1]])
        if not 'unk' in potential_value:
            value = potential_value
    return value

def createOneDataLine(jsonFile, attributes):
    values = list()
    for attribute in attributes:
        values.append(findAttributeValue(jsonFile, attribute))
    line = ",".join(values)
    return line

def createArff(file, jsonFiles, attributes, key):
    for jF in jsonFiles:
        url = jF['analysis_stats'] + "?token=" + key
        analysis = json.loads(curl(url), encoding='iso-8859-1')
        print(analysis)
        file.write(createOneDataLine(analysis, attributes) + ",")
        file.write("{0},{1},{2},".format(jF['bitrate'], jF['bitdepth'], jF['duration']))
        if "human" in jF["tags"] and ("distress" in jF["tags"] or "crying" in jF["tags"]    or "pain" in jF["tags"] or "screaming" in jF["tags"] or "moaning" in jF["tags"] or "scared" in jF["tags"] or "yelling" in jF["tags"]):
            #write to file under Human-In-Distress
            file.write("Human-In-Distress\n")
        else:
            #write to file under Other
            file.write("Other\n")
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

    f = open(OUTPUT_FILE, 'w')

    allAttributes = getAllAttributes()
    writeHeader(f, allAttributes)
    createArff(f,  allJsonForIds, allAttributes, userInput["key"])
    f.close()


if __name__ == "__main__":
    main()
