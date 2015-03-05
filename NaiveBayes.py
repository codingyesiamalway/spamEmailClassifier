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
                if SpamWordNonSpamProb[spamWord] != 0:
                    nonProb += math.log(SpamWordNonSpamProb[spamWord])
                else:
                    nonProb = -999999999999999999999
        logOdds = spamProb - nonProb
        prob = prob + [logOdds > 0]
    return prob

trainingSetSpamFileList, testSetSpamFileList, trainingSetNonSpamFileList, testSetNonSpamFileList = getTrainingTestSet("spamDataset", "nonspamDataset")
spamWordList, SpamWordSpamProb, SpamWordNonSpamProb, spamProbability = getSpamWordList(trainingSetSpamFileList, trainingSetNonSpamFileList, 2, 3)

for i in testSetNonSpamFileList:
    pre = predict([i], SpamWordSpamProb, SpamWordNonSpamProb, spamProbability)
    with open(i) as f:
        print f.read()
    if pre:
        print 'spam'
    else:
        print 'not spam'
    raw_input('press key to continue')


# p = predict(trainingSetNonSpamFileList, SpamWordSpamProb, SpamWordNonSpamProb, spamProbability)
# print sum(p) / float(len(p))  # result is 0.217729393468
# p = predict(trainingSetSpamFileList, SpamWordSpamProb, SpamWordNonSpamProb, spamProbability)
# print sum(p) / float(len(p))  # result is 0.973958333333
# p = predict(testSetSpamFileList, SpamWordSpamProb, SpamWordNonSpamProb, spamProbability)
# print sum(p) / float(len(p))  # 0.975051975052
# p = predict(testSetNonSpamFileList, SpamWordSpamProb, SpamWordNonSpamProb, spamProbability)
# print sum(p) / float(len(p))  # 0.248341625207
#
# spamWordList, SpamWordSpamProb, SpamWordNonSpamProb, spamProbability = getSpamWordList(trainingSetSpamFileList, trainingSetNonSpamFileList, 3, 3)
# p = predict(trainingSetNonSpamFileList, SpamWordSpamProb, SpamWordNonSpamProb, spamProbability)
# print sum(p) / float(len(p))  # 0.191290824261
# p = predict(trainingSetSpamFileList, SpamWordSpamProb, SpamWordNonSpamProb, spamProbability)
# print sum(p) / float(len(p)) # 0.953125
# p = predict(testSetSpamFileList, SpamWordSpamProb, SpamWordNonSpamProb, spamProbability)
# print sum(p) / float(len(p)) # 0.952182952183
# p = predict(testSetNonSpamFileList, SpamWordSpamProb, SpamWordNonSpamProb, spamProbability)
# print sum(p) / float(len(p)) # 0.214759535655

# calculate word list based on minSpamNonSpamCountDiff
def getSpamWordList(trainingSetSpamFileList, trainingSetNonSpamFileList, minSpamNonSpamCountDiff):
    spamTokens = getTokenCountFromTokenList(getNormalizedTokenList(trainingSetSpamFileList))
    nonSpamTokens = getTokenCountFromTokenList(getNormalizedTokenList(trainingSetNonSpamFileList))
    nonSpamTokensDict = dict(nonSpamTokens)
    SpamTokensDict = dict(spamTokens)

    spamWordList =[ i for i in spamTokens if i[1] >= minSpamNonSpamCountDiff and (i[0] not in nonSpamTokensDict or i[1] - nonSpamTokensDict[i[0]]  >= minSpamNonSpamCountDiff) ]

    totalSpamCount = sum([i[1] for i in spamTokens])
    totalNonSpamCount = sum([i[1] for i in nonSpamTokens])

    SpamWordSpamProb = [(i[0], i[1] / float(totalSpamCount)) for i in spamWordList]

    SpamWordNonSpamProb = []
    for i in spamWordList:
        if i[0] in nonSpamTokensDict:
            SpamWordNonSpamProb = SpamWordNonSpamProb + [(i[0], nonSpamTokensDict[i[0]] / float(totalNonSpamCount))]
        else:
            SpamWordNonSpamProb = SpamWordNonSpamProb + [(i[0], 0.0 / float(totalNonSpamCount))]

    spamProbability = float(totalSpamCount) / (totalSpamCount + totalNonSpamCount)
    return spamWordList, dict(SpamWordSpamProb), dict(SpamWordNonSpamProb), spamProbability


