# -*- coding:utf-8 -*-

import csv
from numpy import *
import operator


def loadTrainData():
    data = []
    with open('train.csv') as file:
        lines = csv.reader(file)
        for line in lines:
            data.append(line)
    data.remove(data[0])
    data = array(data)
    label = data[:, 0]
    data = data[:, 1:]
    return normalizing(toInt(data)), toInt(label)


def loadTestData():
    data = []
    with open('test.csv') as file:
        lines = csv.reader(file)
        for line in lines:
            data.append(line)
    data.remove(data[0])
    data = array(data)
    result = normalizing(toInt(data))
    return result

def loadTestResult():
    data = []
    with open('knn_benchmark.csv') as file:
        lines = csv.reader(file)
        for line in lines:
            data.append(line)
    data.remove(data[0])
    data = array(data)
    return normalizing(toInt(data))


def toInt(data):
    data = mat(data)
    m, n = shape(data)
    outData = zeros((m, n))
    for i in range(m):
        for j in range(n):
            outData[i, j] = int(data[i, j])
    return outData


def normalizing(data):
    m, n = shape(data)
    for i in range(m):
        for j in range(n):
            if data[i, j] != 0:
                data[i, j] = 1
    return data

def classify(inX, dataSet, labels, k):
    inX = mat(inX)
    dataSet = mat(dataSet)
    labels = mat(labels)
    dataSize = shape(dataSet)[0]
    copyX = tile(inX, (dataSize, 1))
    diffMat = copyX - dataSet
    sqDifffMat = array(diffMat) ** 2
    sqDistance = sqDifffMat.sum(axis=1)
    distances = sqDistance ** 0.5
    sortedDistanceIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[0, sortedDistanceIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    print '---------------\n'
    print sortedClassCount
    print '---------------\n'
    return sortedClassCount[0][0]


def saveResult(result):
    with open('result.csv', 'wb') as myFile:
        myWriter = csv.writer(myFile)
        for i in result:
            temp = []
            temp.append(i)
            myWriter.writerow(temp)

def formatResult():
    newResult = [];
    with open('result.csv') as file:
         lines = csv.reader(file)
         idx = 1;
         for line in lines:
             line.insert(0, idx)
             #print line[1]
	     #print type(int(line[1]))
             #exit()
             line[1] = int(float(line[1]))
             newResult.append(line)
             idx += 1 
    #print newResult[:20]
    #exit()
    with open('newResult.csv', 'wb') as myFile:
         myWriter = csv.writer(myFile)
         head = ['ImageId', 'Label']
	 #print type(head)
         #print head
         myWriter.writerow(head)
         for i in newResult:
             #print type(i)
             #print i
             #exit()
             myWriter.writerow(i)


def handwritingClassTest():
    trainData, trainLabel = loadTrainData()
    #print trainData[:3,:10]
    #exit()
    testData = loadTestData()
    m, n = shape(testData)
    #print "row=%d, column=%d" % (m, n) 
    #exit()
    resultList = []
    for i in range(m):
        classifierResult = classify(testData[i], trainData, trainLabel, 5)
        resultList.append(classifierResult)
        print "idx= %d, the classifier came back with %d" % (i, classifierResult)
    saveResult(resultList)


#执行函数
#handwritingClassTest()
formatResult()

