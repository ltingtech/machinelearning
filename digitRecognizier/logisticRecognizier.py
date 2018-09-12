# -*- coding:utf-8 -*-


from numpy import *
import csv

def loadDataset():
    data = []
    with open('train.csv') as file:
        lines = csv.reader(file)
        for line in lines:
            data.append(line)
    data.remove(data[0])
    data = array(data)
    label = data[:, 0]
    featureData = data[:, 1:]
    return normalizing(toInt(featureData)), toInt(label)


def loadTestData():
    data = []
    with open('test.csv') as file:
        lines = csv.reader(file)
        for line in lines:
            data.append(line)
    data.remove(data[0])
    data = array(data)
    return normalizing(toInt(data))


def toInt(arrData):
    data = mat(arrData)
    row, column = shape(data)
    newData = zeros((row, column))
    for i in range(row):
        for j in range(column):
            newData[i, j] = int(data[i, j])
    return newData


def normalizing(arrData):
    row, column = shape(arrData)
    newData = zeros((row, column))
    for i in range(row):
        for j in range(column):
            if arrData[i, j] != 0:
                newData[i, j] = 1
    return newData

def sigmod(inX):
    return 1.0 / (1 + exp(-1 *inX))


def changeLabel(label, num):
    newLabel = []
    for labelEle in label[0]:
	if labelEle != num:
            newLabel.append(0)
        else:
            newLabel.append(1)
    return newLabel


def gradAscent(featureData, label):
    arrTheta = []
    featureData = mat(featureData)
    for digitNum in range(10):  #分别对0-9进行逻辑回归训练
        newLabel = changeLabel(label, digitNum)
        newLabel = mat(newLabel).transpose()
        m, n = shape(featureData)
        alpha = 0.001
        maxCycle = 500
        weights = ones((n, 1))
        for k in range(maxCycle):
            test = matrix([[1,2,]])
	    temp = featureData * weights
            h = sigmod(temp)
	    error = newLabel - h
            weights = weights + alpha * featureData.transpose() * error
        weightList = weights.transpose().tolist()[0]
        #print weights.transpose().tolist()[0] 
        #exit()
        arrTheta.append(weightList)

    return arrTheta


def saveResult(result):
    m, n = shape(result)
    with open('logisticResult.csv', 'wb') as file:
        myWriter = csv.writer(file)
        head = ['ImageId', 'Label']
        myWriter.writerow(head)
        for i in range(m):
            line = [i+1]
            line.append(int(result[i, 0]))
            myWriter.writerow(line)


#logistic回归主函数
def logisticRecognizier():
    trainData, trainLabel = loadDataset()
    arrTheta = gradAscent(trainData, trainLabel)
    #print arrTheta
    #print "print matrix theta"    
    #print arrTheta
    #exit()
    testData = loadTestData()
    matTheta = mat(arrTheta)
    testData = mat(testData)
    #print testData
    #print matTheta
    #quit()
    matX = testData * matTheta.transpose()
    #print matX
    matResult = sigmod(matX)
    #print matResult
    #quit()
    m, n = shape(matResult)
    result = matResult.argmax(axis=1)  #求出每行最大值对应的索引位置
    #print result
    #quit()
    saveResult(result)


logisticRecognizier()
