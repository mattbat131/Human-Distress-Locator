import arff
import numpy as np
import codecs
import random

class NearestN:
    def __init__(self, tP):
        self.data = tP
        self.max = 0
        self.maxIndex = 0
        #print(self.data)

    def getDistance(self, tP, p):
        distance = float(0.0)
        #print(tP)
        for i in range(len(tP)):
             #if not (tP[i][j]=="None" or p[i]=="None" or isinstance(tP[i], type(None)) or isinstance(p[i],type(None)) or isinstance(tP[i], str) or isinstance(p[i], str)):
             if isinstance(tP[i], float) and isinstance(p[i], float):
                 distance += np.power((tP[i] + p[i]),2)
        distance = np.sqrt(distance)
        return distance

    def setCollection(self, tP):
        data = tP

    def getMax(self):
        return self.max

    def setMax(self, p):
        if isinstance(self.data[0], np.ndarray):
            for i in range(len(self.data)):
                 print(self.max)
                 pMax = self.getDistance(self.data[i], p)
                 if pMax > self.max:
                     self.max = pMax
                     self.maxIndex = i
        else:
             pMax = self.getDistance(self.data, p)
             if pMax > self.max:
                 self.max = pMax

    def replaceMax(self, tP, p):
         #print(self.data[index] , "Before")
         if isinstance(self.data[0], np.ndarray):
             self.data[self.maxIndex] = tP
         else:
             #print(tP)
             self.data = tP
         #print(self.data[index] , "After")

    def modeOfClass(self):
        humans = 0
        others = 0
        self.data = np.array(self.data, dtype='object')
        #print(self.data)
        if len(self.data[0]) != 1:
             for tP in self.data:
                 #print(tP)
                 if tP[len(tP)-1] == "Human-In-Distress":
                     humans += 1
                 elif tP[len(tP)-1] == "Other":
                     others += 1
        else:
             if self.data[0][len(self.data)-1] == "Human-In-Distress":
                 humas += 1
             else:
                 others += 1
        print(humans , " " , others)
        return humans > others

def GetTheClassificationFromKnn(tPoints, p, k=1):
     initialData = list()
     for i in range(k):
         initialData.append(tPoints[0][i])
     initialData = np.array(initialData, dtype='object')

     collection = NearestN(initialData)

     maxIndex = collection.setMax(p)

     for i in range(len(tPoints)):
         for j in range(len(tPoints[0])):
             if (j>=k):
                 distance = collection.getDistance(tPoints[i][j], p)
                 #print(tP)
                 if distance < collection.getMax():
                     collection.replaceMax(tPoints[i][j], p)

     outputClass = collection.modeOfClass()
     #outputClass = collection.weightedAverageOfClass()

     return outputClass

def createData(file):
     dataset = arff.load(file)
     data = np.array(dataset['data'])
     return data

#randomize cross folds
def crossFold(tP, crossFolds=1):
     crossLength = len(tP)/float(crossFolds)
     crossArray = []
     last = 0.0

     while last < len(tP):
         crossArray.append(tP[int(last):int(last+crossLength)])
         last += crossLength

     return crossArray

def decisionTree(tP):
    return tP

def main():
     file = codecs.open("HumanDistress_Normalize.arff", 'rb', 'utf-8')
     tPoints = createData(file)

     tPoints_decision = decisionTree(tPoints)
     tPoints_fold = crossFold(tPoints_decision, 10)
     #print(tPoints_fold)

     for i in range(len(tPoints_fold)):
         for tP in tPoints_fold[i]:
            # print(tPoints_fold[:i] + tPoints_fold[i:])
             if GetTheClassificationFromKnn(tPoints_fold[:i]+tPoints_fold[i:], tP, 10):
                # print (tP[len(tP)-1])
                 print ("Got Human")
             else:
                 #print (tP[len(tP)-1])
                 print ("Got Other")

if __name__ == "__main__":
     main()
