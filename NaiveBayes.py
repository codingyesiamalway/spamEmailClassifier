__author__ = 'yuzhao'
from Preprocesser import *
import math

def getSpamWordList(trainingSpamTokenList, trainingNonSpamTokenList, minCountSpamForSpam, minCountNonSpamForSpam, minCountSpamForNonSpam, minCountNonSpamForNonSpam):
    spamTokens = getTokenCountFromTokenList(trainingSpamTokenList)
    nonSpamTokens = getTokenCountFromTokenList(trainingNonSpamTokenList)

    nonSpamTokensDict = dict(nonSpamTokens)
    spamTokensDict = dict(spamTokens)

    wordList =[ i for i in spamTokensDict if spamTokensDict[i] >= minCountSpamForSpam and ( i not in nonSpamTokensDict or nonSpamTokensDict[i] <= minCountNonSpamForSpam )]
    moreWords =  [ i for i in nonSpamTokensDict if nonSpamTokensDict[i] >= minCountNonSpamForNonSpam and ( i not in spamTokensDict or spamTokensDict[i] <= minCountSpamForNonSpam )]
    wordList.extend(moreWords)

    totalSpamEmailWordCount = sum([spamTokensDict[i] for i in spamTokensDict if i in wordList])
    totalNonSpamEmailWordCount = sum([nonSpamTokensDict[i] for i in nonSpamTokensDict if i in wordList])

    # this makes sure that the spam distribution and non-spam distribution have the EXACTLY the same words.
    # otherwise, it can be a huge problem
    def getDist(wordList, totalToCountDict, count):
        thisDict = {}
        for i in wordList:
            if i in totalToCountDict:
                thisDict[i] = totalToCountDict[i] / float(count)
            else:
                thisDict[i] = 0.0000000000001
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
        isSpam = math.exp(spamProb) > math.exp(nonSpamProb)
        prob = prob + [isSpam]
        spamProbAll.append(math.exp(spamProb))
        nonSpamProbAll.append(math.exp(nonSpamProb))
    return prob, spamProbAll, nonSpamProbAll


trainingSetSpamFileList, testSetSpamFileList, trainingSetNonSpamFileList, testSetNonSpamFileList = getTrainingTestSet("D:\\projects\\spamEmailClassifier\\spamDataset", "D:\\projects\\spamEmailClassifier\\nonspamDataset")

spamTrainSample = [ trainingSetSpamFileList[i] for i in sorted(random.sample(xrange(len(trainingSetSpamFileList)), 20))]
spamTestSample = [ testSetSpamFileList[i] for i in sorted(random.sample(xrange(len(testSetSpamFileList)), 20))]
noneSpamTrainSample = [ trainingSetNonSpamFileList[i] for i in sorted(random.sample(xrange(len(trainingSetNonSpamFileList)), 20))]
noneSpamTestSample = [ testSetNonSpamFileList[i] for i in sorted(random.sample(xrange(len(testSetNonSpamFileList)), 20))]

trainingSpamTokenList, testSpamTokenList, trainingNonSpamTokenList, testNonSpamTokenList = getNormalizedEmailList(spamTrainSample, spamTestSample, noneSpamTrainSample, noneSpamTestSample)


wordList, wordDistributionInSpam, wordDistributionInNonSpam, spamProbability =  getSpamWordList(trainingSpamTokenList,trainingNonSpamTokenList, 9, 2, 1, 9999999999)
predict(testNonSpamTokenList, wordDistributionInSpam, wordDistributionInNonSpam, spamProbability)
