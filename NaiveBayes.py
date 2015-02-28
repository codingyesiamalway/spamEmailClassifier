__author__ = 'yuzhao'
from Preprocesser import *
import math

# return list of tuples. eg: [('ffa', 183), ('capitalfm', 169), ('floodgate', 100), ... ]
def getSpamWordList(trainingSetSpamFileList, trainingSetNonSpamFileList, minCountSpam, minCountNonSpam):
    spamTokens = getTokenCountFromTokenList(getNormalizedTokenList(trainingSetSpamFileList))
    nonSpamTokens = getTokenCountFromTokenList(getNormalizedTokenList(trainingSetNonSpamFileList))
    nonSpamTokensDict = dict(nonSpamTokens)
    SpamTokensDict = dict(spamTokens)

    nonSpamList = [i[0] for i in nonSpamTokens if i[1] >= minCountNonSpam]
    spamWordList =[ i for i in spamTokens if i[1] >= minCountSpam and i[0] not in nonSpamList]

    totalSpamCount = sum([i[1] for i in spamTokens])
    totalNonSpamCount = sum([i[1] for i in nonSpamTokens])

    SpamWordSpamProb = [(i[0], i[1] / float(totalSpamCount)) for i in spamWordList]


    # Add artificial prior so that probability is not 0 for non-spam
    #totalNonSpamCount = totalNonSpamCount + sum([1 for i in SpamTokensDict if i not in nonSpamTokensDict])
    SpamWordNonSpamProb = []
    for i in spamWordList:
        if i[0] in nonSpamTokensDict:
            SpamWordNonSpamProb = SpamWordNonSpamProb + [(i[0], nonSpamTokensDict[i[0]] / float(totalNonSpamCount))]
        else:
            SpamWordNonSpamProb = SpamWordNonSpamProb + [(i[0], 0.0 / float(totalNonSpamCount))]

    spamProbability = float(totalSpamCount) / (totalSpamCount + totalNonSpamCount)
    return spamWordList, dict(SpamWordSpamProb), dict(SpamWordNonSpamProb), spamProbability


def predict(files, SpamWordSpamProb, SpamWordNonSpamProb, spamProbability):
    emailTokens = getNormalizedTokenList(files)
    prob = []
    for i in emailTokens:
        spamProb = math.log(spamProbability)
        nonProb = math.log(1.0 - spamProbability)
        for spamWord in SpamWordSpamProb:
            if spamWord in i:
                spamProb += math.log(SpamWordSpamProb[spamWord])
                nonProb += math.log(SpamWordNonSpamProb[spamWord])
        logOdds = spamProb - nonProb
        prob = prob + [logOdds > 0]
    return prob



trainingSetSpamFileList, testSetSpamFileList, trainingSetNonSpamFileList, testSetNonSpamFileList = getTrainingTestSet("spamDataset", "nonspamDataset")
spamWordList, SpamWordSpamProb, SpamWordNonSpamProb, spamProbability = getSpamWordList(trainingSetSpamFileList, trainingSetNonSpamFileList, 2, 3)

p = predict(trainingSetNonSpamFileList[:20], SpamWordSpamProb, SpamWordNonSpamProb, spamProbability)
print p