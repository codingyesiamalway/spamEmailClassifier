__author__ = 'Yu Zhao'
from os import listdir
from os.path import isfile, join
import random
import re

def getTrainingTestSet(spamDir, nonSpamDir):
    spamFiles = [ f for f in listdir(spamDir) if isfile(join(spamDir,f)) ]
    trainingSetSpam = map(lambda x: spamDir + '/' + x, random.sample(spamFiles,int(len(spamFiles) * 0.8)))
    testSetSpam = [spamDir + '/' + i for i in spamFiles if i not in trainingSetSpam]

    nonSpamFiles = [ f for f in listdir(nonSpamDir) if isfile(join(nonSpamDir,f)) ]
    trainingSetNonSpam =  map(lambda x: nonSpamDir + '/' + x, random.sample(nonSpamFiles,int(len(nonSpamFiles) * 0.8)))
    testSetNonSpam = [nonSpamDir + '/' + i for i in nonSpamFiles if i not in trainingSetNonSpam]
    return trainingSetSpam, testSetSpam, trainingSetNonSpam, testSetNonSpam


# def createEmailList(spamFile, nonSpamFile):
#     spamEmailList = []
#     with open(spamFile, 'r') as file :
#         curEmail = ''
#         for curLine in file:
#             line = curLine.strip()
#             if line == '----':
#                 if curEmail != "":
#                     spamEmailList = spamEmailList + [curEmail]
#                 curEmail = ''
#             elif curEmail != "":
#                 curEmail = curEmail + ' ' + line
#             else:
#                 curEmail = line
#     return spamEmailList

def getNormalizedTokenList(fileList):
    spamEmailList = []
    for i in fileList:
        with open(i, 'r') as file :
            data=file.read().replace('\n', '').replace('$', ' dollar ').replace('1', ' one ').replace('2', ' two ').replace('3', ' three ').replace('4', ' four ').replace('5', ' five ').replace('6', ' six ').replace('7', ' seven ').replace('8', ' eight ').replace('9', ' nine ').replace('0', ' zero ')

            #re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', 'httpaddr', data, flags=re.MULTILINE)
            re.sub(r'[\w\-][\w\-\.]+[' ']*@[' ']*[\w\-][\w\-\.]+[a-zA-Z]{1,4}', 'emailaddr', data)
            re.sub('[^0-9a-z]+', '', data)
            data = [filter(str.isalnum, i) for i in data.split()]
            data = [i for i in data if i != '' and i != 'Subject']
            spamEmailList = spamEmailList + [data]
    return spamEmailList

def getTokenCountFromTokenList(tokenList):
    dict = {}
    for i in tokenList:
        for j in i:
            if dict.has_key(j):
                dict[j] += 1
            else:
                dict[j] = 1
    #sorted_x = sorted(x.items(), key=operator.itemgetter(1))
    listOfTuples = [(k, v) for k, v in dict.iteritems()]
    return sorted(listOfTuples, key=lambda tup: tup[1],  reverse=True)



# spamSet = getSpamDataSet("spamDataset")
# nonSpamList = [i[0] for i in getTokenCountFromTokenList(getSpamDataSet("nonspamDataset")) if i[1] > 2]
# spam =[ i for i in getTokenCountFromTokenList(spamSet) if i[1] > 1 and i[0] not in nonSpamList]
#
# print len(spam)
# print spam