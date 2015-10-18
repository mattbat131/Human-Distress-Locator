import arff
import numpy as np
import codecs

class NearestN:
    def __init__(self, tP):
        self.data = tP
        self.max = 0
        self.maxIndex = 0

    def getDistance(self, tP, p):
        distance = float(0.0)
        for i in range(len(tP)):
            for j in range(len(tP[i])):
                 if not (isinstance(tP[i][j], type(None)) and isinstance(p[i][j],type(None)) and isinstance(tP[i][j], string) and isinstance(p[i][j], string)):
                     distance += (tP[i][j] + p[i][j]) * (tp[i][j] + p[i][j])
        distance = np.sqrt(distance)
        return distance

    def setCollection(self, tP):
        data = tP

    def getMax(self):
        return self.max

    def setMax(self, p):
        i = 0
        if isinstance(self.data[0], list):
             for tP in self.data:
                 pMax = self.getDistance(tP, p)
                 i+=1
                 if pMax > self.max:
                     self.max = pMax
                     self.maxIndex = i
        else:
             pMax = self.getDistance(self.data, p)
             if pMax > self.max:
                 self.max = pMax
        return i

    def replaceMax(self, tP, p, index):
        if isinstance(self.data[0], list):
            self.data[index] = tP
        else:
            self.data = tP
        return self.setMax(p)

    def modeOfClass(self):
        humans = 0
        others = 0
        if isinstance(self.data[0], list):
             for tP in self.data:
                 if tP[len(tP)-1] == "Human-In-Distress":
                     humans += 1
                 elif tp[len(tP)-1] == "Other":
                     others += 1
        else:
             print(self.data[len(self.data)-1])
             if self.data[len(self.data)-1] == "Human-In-Distress":
                 humas += 1
             else:
                 others += 1
        return humans > others

def GetTheClassificationFromKnn(tPoints, p, k=1):
     initialData = list()
     for i in range(k):
         initialData.append(tPoints[i])
     initialData = np.array(initialData, dtype='object')

     collection = NearestN(initialData)

     maxIndex = collection.setMax(p)

     for tP in tPoints:
        distance = collection.getDistance(tP, p)

        if distance < collection.getMax():
            maxIndex = collection.replaceMax(tP, p, maxIndex)

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

     for i in range(len(tPoints_fold)):
         for tP in tPoints_fold[i]:
             if GetTheClassificationFromKnn(tPoints_fold[np.arange(len(tPoints_fold)!=i)], tP, 10):
                 print (tP[len(tP)-1])
                 print ("Got Human")
             else:
                 print (tP[len(tP)-1])
                 print ("Got Other")

if __name__ == "__main__":
     main()
