#-*- coding:utf-8-*-

from numpy import *
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

'''
def loadDataset():
	dataMat = matrix([[1., 2.1],
	[2., 1.1],
	[1.3, 1.],
	[1., 1.],
	[2., 1.]])
	classLabels = [1.0, 1.0, -1.0, -1.0, 1.0]
	return dataMat, classLabels
'''

def loadDataset(fileName):
	numFeat = len(open(fileName).readline().split('\t'))
	dataMat = []
	classLabels = []
	fr = open(fileName)
	for line in fr.readlines():
		lineArr = []
		curLine = line.strip().split('\t')
		for i in range(numFeat -1):
			lineArr.append(float(curLine[i]))
		dataMat.append(lineArr)
		classLabels.append(float(curLine[-1]))
	return dataMat, classLabels
	
	


def stumpClassify(dataMatrix, dimen, threshVal, threshIneq):
	retArray = ones((shape(dataMatrix)[0], 1))
	if threshIneq == 'lt':
		retArray[dataMatrix[:, dimen] <= threshVal] = -1.0
	else:
		retArray[dataMatrix[:, dimen] >= dimen] = -1.0
	return retArray

def buildStump(dataArr, classLabels, weightD):
	dataMatrix = mat(dataArr)
	labelMat = mat(classLabels).T
	m, n = shape(dataMatrix)
	numSteps = 10.0
	bestStump = {}
	bestClassEst = mat(zeros((m, 1)))
	minError = inf
	for i in range(n):
		rangeMin = dataMatrix[:, i].min()
		rangeMax = dataMatrix[:, i].max()
		stepSize = (rangeMax - rangeMin) / numSteps
		for j in range(-1, int(numSteps) + 1) :
			for inequal in ['lt', 'gt']:
				threshVal = rangeMin + stepSize * j
				predictVals = stumpClassify(dataMatrix, i, threshVal, inequal)
				errArr = mat(ones([m, 1]))
				errArr[predictVals == labelMat] = 0
				weightError = weightD.T * errArr
				#print "split: dim %d, thresh: %.2f, threshIneq: %s, the weightError is %.3f, " % (i, threshVal, inequal, weightError)
				if weightError < minError:
					minError = weightError
					bestClassEst = predictVals.copy()
					bestStump['dim'] = i
					bestStump['thresh'] = threshVal
					bestStump['ineq'] = inequal
	return bestStump, minError, bestClassEst
		

def adaBoostTrainDs(dataArr, classLabels, numIt=40):
	weakClassArr = []
	m = shape(dataArr)[0]
	D = mat(ones((m, 1))) / m   # 初始权重
	aggClassEst = mat(zeros((m, 1)))
	for i in range(numIt):
		bestStump, error, classEst = buildStump(dataArr, classLabels, D)
		print "weightD : ", D.T
		alpha = float(0.5 * log((1 - error) / max(error, 1e-16)))
		bestStump['alpha'] = alpha
		weakClassArr.append(bestStump)
		print "classEst:", classEst.T
		expon = multiply(-1 * alpha * mat(classLabels).T, classEst)
		D = multiply(D, exp(expon))
		D = D / D.sum()
		aggClassEst += alpha * classEst   # 计算结果集成算法的结果
		print "aggClassEst : ", aggClassEst.T
		aggError = multiply(sign(aggClassEst) != mat(classLabels).T, ones((m, 1)))
		errRate = aggError.sum() / m
		print "total errorRate : ", errRate, "\n"
		if errRate == 0.0: break
	return weakClassArr, aggClassEst

def adaClassify(testData, classifier):
	dataMat = mat(testData)
	m = shape(dataMat)[0]
	aggClassEst = mat(zeros((m, 1)))
	for i in range(len(classifier)):
		classEst = stumpClassify(dataMat, classifier[i]['dim'], classifier[i]['thresh'], classifier[i]['ineq'])
		aggClassEst += classifier[i]['alpha'] * classEst
		print aggClassEst.T
	return sign(aggClassEst)


def plotRoc(predStrengths, classLabels):
	cur = (1.0, 1.0)
	ySum = 0.0
	numPosClass = sum(array(classLabels) == 1.0)
	yStep = 1 / float(numPosClass)
	xStep = 1 / float(len(classLabels) - numPosClass)
	sortedIndices = predStrengths.argsort()
	fig = plt.figure()
	fig.clf()
	ax = plt.subplot(111)
	for index in sortedIndices.tolist()[0]:
		if classLabels[index] == 1.0:
			delX = 0
			delY = yStep
		else:
			delX = xStep
			delY = 0
			ySum += cur[1]
		ax.plot([cur[0], cur[0] - delX], [cur[1], cur[1] - delY], c='b')
		cur = (cur[0] - delX, cur[1] - delY)
	ax.plot([0, 1], [0, 1], 'b--')
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.title('ROC curve for Adaboost Horse Colic')
	ax.axis([0, 1, 0, 1])
	plt.savefig('roc.png');
	plt.close()
	print "the Area Under the Curve is: ", ySum * xStep	 



dataMat, classLabels = loadDataset('horseColicTest2.txt')
#print dataMat
#print classLabels
#weightD = mat(ones((shape(dataMat)[0], 1)) / 5)
#bestStump, minError, bestClassEst = buildStump(dataMat, classLabels, weightD)
#print minError
#print bestClassEst
classifierArr, aggClassEst = adaBoostTrainDs(dataMat, classLabels, 9)
print classifierArr
#测试下
#testRet = adaClassify([0, 0], classifierArr)
#print testRet
testData, testLabels = loadDataset('horseColicTest2.txt')
testRet = adaClassify(testData, classifierArr)
m = shape(mat(testData))[0]
errArr = mat(ones((m, 1)))
errArr[testRet == mat(testLabels).T] = 0
totalError = errArr.sum()
print "total error: ", totalError
errRate = float(1.0 * totalError / m)
print "errRate: ", errRate

plotRoc(aggClassEst.T, classLabels)




