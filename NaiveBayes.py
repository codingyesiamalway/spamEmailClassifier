__author__ = 'yuzhao'
from Preprocesser import *
import math

# returned probability distrbution is prior adjusted and has no zero value
def getSpamWordList(trainingSpamTokenList, trainingNonSpamTokenList, minCountSpamForSpam, minCountNonSpamForSpam, minCountSpamForNonSpam, minCountNonSpamForNonSpam):
    spamTokens = getTokenCountFromTokenList(trainingSpamTokenList)
    nonSpamTokens = getTokenCountFromTokenList(trainingNonSpamTokenList)

    nonSpamTokensDict = dict(nonSpamTokens)
    spamTokensDict = dict(spamTokens)

    wordList =[ i for i in spamTokensDict if spamTokensDict[i] >= minCountSpamForSpam and ( i not in nonSpamTokensDict or nonSpamTokensDict[i] <= minCountNonSpamForSpam )]
    moreWords =  [ i for i in nonSpamTokensDict if nonSpamTokensDict[i] >= minCountNonSpamForNonSpam and ( i not in spamTokensDict or spamTokensDict[i] <= minCountSpamForNonSpam )]
    wordList.extend(moreWords)

    # add prior to spamTokensDict to adjust for zero prob
    def adjustCount(wordDict, wordList):
        for i in wordList:
            if i in wordDict and wordDict[i] == 0:
                wordDict[i] = 1

    adjustCount(spamTokensDict, wordList)
    adjustCount(nonSpamTokensDict, wordList)

    totalSpamEmailWordCount = sum([spamTokensDict[i] for i in spamTokensDict if i in wordList])
    totalNonSpamEmailWordCount = sum([nonSpamTokensDict[i] for i in nonSpamTokensDict if i in wordList])

    def getDist(wordList, totalToCountDict, count):
        thisDict = {}
        for i in wordList:
            if i in totalToCountDict:
                thisDict[i] = totalToCountDict[i] / float(count)
        return thisDict

    wordDistributionInSpam = getDist(wordList, spamTokensDict, totalSpamEmailWordCount)
    wordDistributionInNonSpam = getDist(wordList, nonSpamTokensDict, totalNonSpamEmailWordCount)

    spamProbability = float(totalSpamEmailWordCount) / (totalSpamEmailWordCount + totalNonSpamEmailWordCount)
    return wordList, wordDistributionInSpam, wordDistributionInNonSpam, spamProbability


# assume dist has no zero probability
def predict(emailTokenList, wordDistributionInSpam, wordDistributionInNonSpam, spamProbability):
    prob = []
    spamProbAll = []
    nonSpamProbAll = []
    for email in emailTokenList:
        spamProb = math.log(spamProbability)
        nonSpamProb = math.log(1.0 - spamProbability)
        for j in email:
            if j in wordDistributionInSpam:
                spamProb += math.log(wordDistributionInSpam[j])
            if j in wordDistributionInNonSpam:
                nonSpamProb += math.log(wordDistributionInNonSpam[j])
        isSpam = spamProb > nonSpamProb
        prob = prob + [isSpam]
        spamProbAll.append(spamProb)
        nonSpamProbAll.append(nonSpamProb)
    return prob, spamProbAll, nonSpamProbAll


trainingSetSpamFileList, testSetSpamFileList, trainingSetNonSpamFileList, testSetNonSpamFileList = getTrainingTestSet("D:\\projects\\spamEmailClassifier\\spamDataset", "D:\\projects\\spamEmailClassifier\\nonspamDataset")
trainingSpamTokenList, testSpamTokenList, trainingNonSpamTokenList, testNonSpamTokenList = getNormalizedEmailList(trainingSetSpamFileList, testSetSpamFileList, trainingSetNonSpamFileList, testSetNonSpamFileList)

wordList, wordDistributionInSpam, wordDistributionInNonSpam, spamProbability =  getSpamWordList(trainingSpamTokenList,trainingNonSpamTokenList, 9, 2, 1, 9)
predict(testNonSpamTokenList, wordDistributionInSpam, wordDistributionInNonSpam, spamProbability)
