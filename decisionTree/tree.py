# -*- coding:utf-8 -*-

from math import log
import operator
import plotTree
import pickle

#给定数据集，计算香农熵
def calcShannonEnt(dataset):
	entriesNum = len(dataset)
	labelCount = {}
	for featVec in dataset:
		label = featVec[-1]
		if label not in labelCount.keys():
			labelCount[label] = 0
		labelCount[label] += 1
	shannonEnt = 0.0
	for key in labelCount:
		prob = float(labelCount[key]) / entriesNum
		shannonEnt -= prob * log(prob, 2)
	return shannonEnt

#根据某个特征是否等于特征值，提取出符合条件的数据子集
def splitDataset(dataset, axis, value):
	reducedDataset = []
	for featVec in dataset:
		if featVec[axis] == value:
			reduceFeatVec = featVec[:axis]
			reduceFeatVec.extend(featVec[axis+1:])
			reducedDataset.append(reduceFeatVec)
	return reducedDataset

#选取最优的特征，这里采用的是信息增益判别标准，也可以采用信息增益比进行判别
def chooseBestFeatureToSplit(dataset):
	featNum = len(dataset[0]) - 1
	bestFeatIdx = -1
	bestInfoGain = 0.0
	baseShannonEnt = calcShannonEnt(dataset)
	for idx in range(featNum):
		featList = [example[idx] for example in dataset]
		uniqVals = set(featList)
		newEntropy = 0.0
		for value in uniqVals:	
			subDataset = splitDataset(dataset, idx, value)
			prob = len(subDataset) / float(len(dataset))
			newEntropy += prob * calcShannonEnt(subDataset)
		infoGain = baseShannonEnt - newEntropy
		if (infoGain > bestInfoGain):
			bestInfoGain = infoGain
			bestFeatIdx = idx
	return bestFeatIdx
			

#根据信息增益比确定最优的分裂特征
def chooseBestFeatureToSplitV2(dataset):
	featNum = len(dataset[0]) -1
	bestFeatIdx = -1
	bestGainRatio = 0.0
	baseShannonEnt = calcShannonEnt(dataset)
	for idx in range(featNum):
		featureList = [example[idx] for example in dataset]
		uniqVals = set(featureList)
		newEntropy = 0.0
		splitInfomation = 0.0
		for value in uniqVals:
			subDataset = splitDataset(dataset, idx, value)
			prob = len(subDataset) / float(len(dataset))
			newEntropy -= prob * calcShannonEnt(subDataset)
			splitInfomation -= prob * log(prob, 2)
		infoGain = baseShannonEnt - newEntropy
		gainRatio = infoGain / splitInfomation
		#print "feature idx :%d, gainRatio:%f" % (idx, gainRatio)
		if (gainRatio > bestGainRatio):
			bestGainRatio = gainRatio
			bestFeatIdx = idx

	return bestFeatIdx

def createDataset():
	'''
	dataset = [[1, 1, 'yes'],
			[1, 1, 'yes'],
			[1, 0, 'no'],
			[0, 1, 'no'],
			[0, 1, 'no']]
	labels = ['no surfacing', 'flippers']
	'''
	fr = open('lenses.txt')
	dataset = [strLine.strip().split('\t') for strLine in fr.readlines()]
	labels = ['age', 'prescript', 'astigmatic', 'tearRate']
	
	return dataset, labels

# 如果到达叶子节点仍然不属于同一类，则按多数投票进行表决
def majorityVote(classList):
	classCount = {}
	for vote in classList:	
		if vote not in classCount.keys():
			classCount[vote] = 0
		classCount[vote] += 1
	sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedClassCount[0][0]


# 生成决策树
def createTree(dataset, labels):
	classList = [example[-1] for example in dataset]
	if classList.count(classList[0]) == len(classList):  # 如果已经属于一类
		return classList[0]
	if (len(dataset[0]) == 1) :    # 如果遍历完所有的特征
		return majorityVote(classList)
	bestFeatIdx = chooseBestFeatureToSplit(dataset)
	bestLabel = labels[bestFeatIdx]
	myTree = {bestLabel:{}}
	del(labels[bestFeatIdx])
	featValues = [example[bestFeatIdx] for example in dataset]
	uniqVals = set(featValues)
	for value in uniqVals:
		subDataset = splitDataset(dataset, bestFeatIdx, value)
		subLabels = labels[:]
		myTree[bestLabel][value] = createTree(subDataset, subLabels)
	return myTree


def classify(myTree, labels, dataVect):
	firstStr = myTree.keys()[0]
	secondDict = myTree[firstStr]
	featIdx = labels.index(firstStr)
	for key in secondDict.keys():
		if key == dataVect[featIdx]:
			if type(secondDict[key]).__name__ == 'dict':
				classLabel = classify(secondDict[key], labels, dataVect)
			else:
				classLabel = secondDict[key]
	return classLabel 


def storeTree(myTree, filename):
	fw = open(filename, 'w')
	pickle.dump(myTree, fw)
	fw.close()
	
def grabTree(filename):
	fr = open(filename)	
	return pickle.load(fr)
	


dataset, labels = createDataset()
#shannonEnt = calcShannonEnt(dataset)
#print shannonEnt
#reduDataset = splitDataset(dataset, 0, 0)
#print reduDataset
#bestFeatIdx = chooseBestFeatureToSplitV2(dataset)
#print bestFeatIdx
#print dataset
copyLabels = []
for label in labels:
	copyLabels.append(label)
tree = createTree(dataset, copyLabels);
print tree
#classLabel = classify(tree, labels, [1, 0])
#print classLabel
#classLabel = classify(tree, labels, [1, 1])
#print classLabel
plotTree.createPlot(tree)
#treeFile = 'storeTree.txt'
#storeTree(tree, treeFile)
#rebuildTree = grabTree(treeFile)
#print rebuildTree









