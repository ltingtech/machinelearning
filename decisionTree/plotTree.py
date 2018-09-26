# -*-coding:utf-8 -*-
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")

def plotNode(nodeTxt, centerPt, parentPt, nodeType):	
	createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords="axes fraction", xytext=centerPt, textcoords="axes fraction", \
			 va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)
	

def createPlot():
	fig = plt.figure(1, facecolor='white')
	fig.clf()
	createPlot.ax1 = plt.subplot(111, frameon=False)
	plotNode("decisionNode", (0.5, 0.1), (0.1, 0.5), decisionNode)
	plotNode("leafNode", (0.8, 0.1), (0.3, 0.8), leafNode)
	plt.savefig('tree.png')
	plt.close()

# 获取树的叶子节点数量
def getLeafNum(myTree):
	leafNum = 0
	firstStr = myTree.keys()[0]
	secondStr = myTree[firstStr]
	for key in secondStr.keys():
		if type(secondStr[key]).__name__ == 'dict':
			leafNum += getLeafNum(secondStr[key])
		else: leafNum += 1

	return leafNum 

# 获取树的深度
def getTreeDepth(myTree):
	maxDepth = 0
	firstStr = myTree.keys()[0]
	secondStr = myTree[firstStr]
	myDepth = 0
	for key in secondStr.keys():
		if (type(secondStr[key]).__name__ == 'dict'):
			myDepth = 1 + getTreeDepth(secondStr[key])
		else: myDepth = 1
		if myDepth > maxDepth : 
			maxDepth = myDepth
	
	return maxDepth

def plotMidText(cntrNode, parentNode, stringText):
	xMid = (parentNode[0] - cntrNode[0]) / 2.0 + cntrNode[0]
	yMid = (parentNode[1] - cntrNode[1]) / 2.0 + cntrNode[1]  
	textArgs = dict(rotation=45, va='center', ha='center')	
	createPlot.ax1.text(xMid, yMid, stringText, **textArgs)

# 绘制树节点
def plotTree(myTree, parentNode, strTxt):
	figureHeight = 1    #设定图片占整张图的高度比例，防止最下面的那层被削底
	treeDepth = getTreeDepth(myTree)
	leafNum = getLeafNum(myTree)
	cntrNode = (plotTree.xOff + (leafNum + 1) / 2.0 / plotTree.totalW, plotTree.yOff)
	attrStr = myTree.keys()[0]
	# 绘制子节点和父节点之间的连线
	plotNode(attrStr, cntrNode, parentNode, decisionNode)  #程序设计的遍历结构能保证当前myTree是一棵树，而不会是一个叶子节点
	plotMidText(cntrNode, parentNode, strTxt)
	plotTree.yOff = plotTree.yOff - figureHeight / plotTree.totalDepth
	childTree = myTree[attrStr]
	for key in childTree.keys():
		if type(childTree[key]).__name__ == 'dict':
			plotTree(childTree[key], cntrNode, str(key))
		else:
			plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
			plotNode(childTree[key], (plotTree.xOff, plotTree.yOff), cntrNode, leafNode)
			plotMidText((plotTree.xOff, plotTree.yOff), cntrNode, str(key))
	plotTree.yOff = plotTree.yOff + figureHeight / plotTree.totalDepth


def createPlot(myTree):
	fig = plt.figure(1, facecolor='white')
	fig.clf()
	axprops = dict(xticks = [], yticks = [])
	createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
	plotTree.totalW = float(getLeafNum(myTree))
	plotTree.totalDepth = float(getTreeDepth(myTree))
	plotTree.xOff = -0.5 / plotTree.totalW
	plotTree.yOff = 1.0
	plotTree(myTree, (0.5, 1.0), '')
	plt.savefig('resultTree.png')
	plt.close()



