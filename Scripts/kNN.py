import arff
import numpy as np
import codecs

def GetTheClassificationFromKnn(tPoints, p, k=1):
     collection = NearestN()

     collection.setCollection([tPoints[i] for i in range(k)])

     maxIndex = collection.setMax(p)

     for tP in tPoints:
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

def crossFold(tP, crossFolds=1):
     crossLength = len(tP)/float(crossFolds)
     crossArray = []
     last = 0.0

     while last < len(tP):
         crossArray.append(tP[int(last):int(last+avg)])
         last += avg

     return crossArray

def main():
     file = codecs.open("HumanDistress_Normalize.arff", 'rb', 'utf-8')
     tPoints = createData(file)

     pFile = codecs.open("Point.arff", 'rb', 'utf-8')
     point = createData(pFile)

     tPoints_fold = crossFold(tP, 10)

     human = 0
     other = 0
     for pts in tPoints_fold:
         if GetTheClassificationFromKnn(tps, p, 1):
             human += 1
         else:
             other += 1
     print(human>other)

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
