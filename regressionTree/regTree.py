# -*-coding:utf-8-*-

from numpy import *


def loadDataset(fileName):
	dataMat = []
	fr = open(fileName)
	for line in fr.readlines():
		curline = line.strip().split('\t')
		fltline = map(float, curline)   # 将所有的数据转化成float型
		dataMat.append(fltline)
	return mat(dataMat)

# 根据某个特征值对数据进行二分
def binSplitDataset(dataset, featureIdx, value):
	mat0 = dataset[nonzero(dataset[:, featureIdx] > value)[0], :]
	mat1 = dataset[nonzero(dataset[:, featureIdx] <= value)[0], :]
	return mat0, mat1

def regLeaf(dataset):
	return mean(dataset[:, -1])

def regErr(dataset):
	return var(dataset[:, -1]) * shape(dataset)[0]  #平方误差

def createTree(dataset, leafType=regLeaf, errType=regErr, ops=(1, 4)):
	featIdx, val = chooseBestSplit(dataset, leafType, errType, ops)
	if featIdx == None:
		return val
	retTree = {}
	retTree['spIdx'] = featIdx
	retTree['spVal'] = val
	lefSet, rigSet = binSplitDataset(dataset, featIdx, val)
	retTree['left'] = createTree(lefSet, leafType, errType, ops)
	retTree['right'] = createTree(rigSet, leafType, errType, ops)
	return retTree

def chooseBestSplit(dataset, leafType=regLeaf, errType=regErr, ops=(1, 4)):
	tolMinGain = ops[0]
	tolMinNum = ops[1]
	bestGain = inf
	baseVar = errType(dataset)
	if (len(set(dataset[:, -1].T.tolist()[0])) == 1):
		return None, leafType(dataset)
	rows, columns = shape(dataset)
	bestFeatIdx = -1;
	bestVal = 0
	for featIdx in range(columns - 1):
		for featVal in set(dataset[:, featIdx].T.tolist()[0]):
			mat0, mat1 = binSplitDataset(dataset, featIdx, featVal)
			if (shape(mat0)[0] < tolMinNum or shape(mat1)[0] < tolMinNum):
				continue
			errMat0 = errType(mat0)
			errMat1 = errType(mat1)
			errGain = errMat0 + errMat1
			if errGain < bestGain:
				bestGain = errGain
				bestFeatIdx = featIdx
				bestVal = featVal
	if (baseVar - bestGain) < tolMinGain:
		return None, leafType(dataset)
	leftMat, rightMat = binSplitDataset(dataset, bestFeatIdx, bestVal)
	if (shape(leftMat)[0] < tolMinNum) or (shape(rightMat)[0] < tolMinNum):
		return None, leafType(dataset)
	return bestFeatIdx, bestVal

def isTree(obj):
	if type(obj).__name__ == 'dict':
		return True
	else:
		return False	
					
def getMean(myTree):
	if isTree(myTree['left']):
		myTree['left'] = getMean(myTree['left'])
	if isTree(myTree['right']):
		myTree['right'] = getMean(myTree['right'])
	return (myTree['left'] + myTree['right']) / 2.0

# 后剪枝
def prune(myTree, testData):
	if shape(testData)[0] == 0 :
		return getMean(myTree)   #如果测试数据在该子树上没有数据，则直接对子树进行塌陷处理
	leftSet, rightSet = binSplitDataset(testData, myTree['spIdx'], myTree['spVal'])
	if isTree(myTree['left']): 
		myTree['left'] = prune(myTree['left'], leftSet)	
	if isTree(myTree['right']):
		myTree['right'] = prune(myTree['right'], rightSet)
	if not isTree(myTree['left']) and not isTree(myTree['right']):
		errNoMerge = sum(power(leftSet[:, -1] - myTree['left'], 2)) + sum(power(rightSet[:, -1] - myTree['right'], 2))
		#treeMean = (getMean(myTree['left']) + getMean(myTree['right'])) / 2.0
		treeMean = getMean(myTree)
		errMerge = sum(power(testData[:, -1] - treeMean, 2))
		if errMerge < errNoMerge:
			print 'merging'
			return treeMean
		else:
			return myTree
	return myTree

# 线性回归模型
def lineSolve(dataset):
	m, n  = shape(dataset)
	X = mat(ones((m, n)))
	Y = mat(ones((m, 1)))
	X[:, 1:n] = dataset[:, 0:n-1]
	Y = dataset[:, -1]
	XTX = X.T * X
	if (linalg.det(XTX) == 0.0) :
		raise NameError('The matrix is singular, cannot do reverse\n\
		try increasing the second value of ops')
	ws = XTX.I * X.T * Y
	return ws, X, Y


def modelLeaf(dataset):
	ws, X, Y = lineSolve(dataset)
	return ws


def modelErr(dataset):
	ws, X, Y = lineSolve(dataset)
	yHat = X * ws
	return sum(power(Y - yHat, 2))
		

'''
#回归树测试代码
#dataset = mat(eye(4))
dataset = loadDataset('ex2.txt')
#mat0, mat1 = binSplitDataset(dataset, 2, 0.6)
#print mat0
#print mat1
tree = createTree(dataset, ops=(1, 4))
print tree
print '--' * 40

testDataset = loadDataset('ex2test.txt')
prunedTree = prune(tree, testDataset)
print prunedTree
'''
#模型树测试代码

dataset = loadDataset('exp2.txt')
tree = createTree(dataset, modelLeaf, modelErr, (1, 10))
print tree

