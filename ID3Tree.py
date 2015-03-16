__author__ = 'Yu Zhao'

# use trainingMatrix.tolist() as traning vectors and y.tolist() as lables
import math
import operator
def calInformationCon(labels):
    labelCounts = {}
    totalCount = 0
    for i in labels:
        totalCount += 1
        if i in labelCounts:
            labelCounts[i] += 1
        else:
            labelCounts[i] = 1

    infoCont = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / totalCount
        infoCont += -1 * prob * math.log(prob, 2)
    return infoCont

def splitDataByFeaturePosAndFeatureFilter(dataSet, labels, featurePos, f):
    retDataSet = []
    retLabel = []
    i = 0
    for row in dataSet:
        if f(row[featurePos]):
            reduced = row[:featurePos]
            reduced.extend(row[featurePos + 1:])
            retDataSet.append(reduced)
            retLabel += [labels[i]]
        i += 1
    return retDataSet, retLabel

def chooseBestFeatureIndexToSplit(dataSet, labels):
    baseInfoContent = calInformationCon(labels)
    bestFeature = -1
    bestEntropy = -1
    for i in range(len(dataSet[0])):
        featureVals = [row[i] for row in dataSet]
        featureSet = set(featureVals)
        newEntropy = 0.0
        for featureVal in featureSet:
            splitData, splitLabels = splitDataByFeaturePosAndFeatureFilter(dataSet, labels, i, lambda x : x == featureVal)
            prob = float(len(splitData)) / len(dataSet)
            newEntropy += prob * calInformationCon(splitLabels)
            if newEntropy > bestEntropy:
                bestEntropy = newEntropy
                bestFeature = i
    return bestFeature


def createTree(dataSet, labels, wordList):
    res = {}
    if labels.count(labels[0]) == len(labels):
        if labels[0]:
            res[-1] = 1
        else:
            res[-1] = -1
        return res
    if len(dataSet[0]) == 1:  # only one feature left, return majority Count
        distinctElements = set(i[0] for i in dataSet)
        labelCount = {}
        for i in distinctElements:
            if i in labelCount:
                labelCount[i] += 1
            else:
                labelCount[i] = 1

        sortedByValue = sorted(labelCount.iteritems(), key = operator.itemgetter(1), reverse=True)
        if sortedByValue[0][0]:
            res[-1] = 1
        else:
            res[-1] = -1
        return res

    else:
        splitFeatureIndex = chooseBestFeatureIndexToSplit(dataSet, labels)
        id3Tree = {wordList[splitFeatureIndex]:{}}
        splitFeatureVals = set([ row[splitFeatureIndex] for row in dataSet])
        for i in splitFeatureVals:
            subData, subLabels = splitDataByFeaturePosAndFeatureFilter(dataSet, labels, splitFeatureIndex, lambda x: x == i)
            nextWordList = wordList[:splitFeatureIndex] + wordList[splitFeatureIndex+1:]
            id3Tree[wordList[splitFeatureIndex]][i] = createTree(subData, subLabels, nextWordList)
        return id3Tree

def predict(emailVector, tree, wordList):
    if -1 in tree:
        return tree[-1]
    else:
        for splitWord in tree:
            wordIndex = wordList.index(splitWord)
            if emailVector[wordIndex] in tree[splitWord]:
                value = emailVector[wordIndex]
                return predict(emailVector, tree[splitWord][value], wordList)