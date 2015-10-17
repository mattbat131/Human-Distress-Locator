import arff
import numpy as np
import codecs

def GetTheClassificationFromKnn(tPoints, p, k=1):
     collection = NearestN()

     collection.setCollection([tPoints['data'][i] for i in range(k)])

     maxIndex = collection.setMax(p)

     for tP in tPoints['data']:
        distance = collection.GetDistance(tP, p)

        if distance < collection.max():
            maxIndex = collection.replaceMax(tP, p, maxIndex)

     outputClass = collection.modeOfClass()
     #outputClass = collection.weightedAverageOfClass()

     return outputClass

def createData(file):
     dataset = arff.load(file)
     data = np.array(dataset['data'])
     return data

def main():
     file = codecs.open("HumanDistress_Normalize.arff", 'rb', 'utf-8')
     tPoints = createData(file)

     pFile = codecs.open("Point.arff", 'rb', 'utf-8')
     point = createData(pFile)

     print(GetTheClassificationFromKnn(tPoints, p, 1))

if __name__ == "__main__":
     main()


class NearestN:
    max = 0
    maxIndex = 0
    data = list()

    def getDistance(tP, p):
        distance = 0
        for i in range(len(tP)-1):
            for j in range(len(tP[1])-2):
                if tP[i][j] != "?" or p[i][j] != "?":
                    distance += np.power(data[i][j] + p[i][j], 2)
        distance = np.sqrt(distance)
        return distance

    def setCollection(tP):
        data = tP

    def setMax(p):
        i = 0
        for tP in data:
            pMax = getDistance(tP, p)
            i+=1
            if pMax > max:
                max = pMax
                maxIndex = i
        return i

    def replaceMax(tP, p, index):
        data[index] = tP
        return setMax(p)

    def modeOfClass():
        humans = 0
        others = 0
        for tP in data:
            if tP[len(tP)-1] == "Humans-In-Distress":
                humans += 1
            elif tp[len(tP)-1] == "Other":
                others += 1
        return humans > others
