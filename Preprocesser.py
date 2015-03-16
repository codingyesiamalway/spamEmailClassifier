__author__ = 'Yu Zhao'
from os import listdir
from os.path import isfile, join
import random
import re
from stemming.porter2 import stem

def getTrainingTestSet(spamDir, nonSpamDir):
    spamFiles = [ f for f in listdir(spamDir) if isfile(join(spamDir,f)) ]
    trainingSetSpam = map(lambda x: spamDir + '/' + x, random.sample(spamFiles,int(len(spamFiles) * 0.8)))
    testSetSpam = [spamDir + '/' + i for i in spamFiles if i not in trainingSetSpam]

    nonSpamFiles = [ f for f in listdir(nonSpamDir) if isfile(join(nonSpamDir,f)) ]
    trainingSetNonSpam =  map(lambda x: nonSpamDir + '/' + x, random.sample(nonSpamFiles,int(len(nonSpamFiles) * 0.8)))
    testSetNonSpam = [nonSpamDir + '/' + i for i in nonSpamFiles if i not in trainingSetNonSpam]
    return trainingSetSpam, testSetSpam, trainingSetNonSpam, testSetNonSpam


def getNormalizedEmailList(trainingSetSpam, testSetSpam, trainingSetNonSpam, testSetNonSpam):
    def readFileListAndNormalize(fileList):
        res = []
        for i in fileList:
            with open(i, 'r') as file :
                data=file.read()
                res = res + [getTokensFromStr(data)]
        return res
    return readFileListAndNormalize(trainingSetSpam), readFileListAndNormalize(testSetSpam), readFileListAndNormalize(trainingSetNonSpam), readFileListAndNormalize(testSetNonSpam)


def readFileListAndNormalize(fileList):
    res = []
    for i in fileList:
        with open(i, 'r') as file :
            data=file.read()
            res = res + [data]
    return res

def getTokensFromStr(email):
    p = re.compile(r'\w*\s*@\s\w*\s*.\s*\w*')
    email = p.sub('emailaddr', email)
    p = re.compile('\d*\W*(\d{3})\D*(\d{3})\D*(\d{4})')
    email = p.sub('phoneNum', email)
    email = email.replace('\n', '').replace('$', ' dollar ').replace('1', ' one ').replace('2', ' two ').replace('3', ' three ').replace('4', ' four ').replace('5', ' five ').replace('6', ' six ').replace('7', ' seven ').replace('8', ' eight ').replace('9', ' nine ').replace('0', ' zero ')
    #re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', 'httpaddr', data, flags=re.MULTILINE)

    re.sub('[^0-9a-z]+', '', email)
    data = [filter(str.isalnum, i) for i in email.split()]
    data = [stem(i) for i in data if i != '' and i != 'Subject']
    return data


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
#
# trainingSetSpamFileList, testSetSpamFileList, trainingSetNonSpamFileList, testSetNonSpamFileList = getTrainingTestSet("D:\\projects\\spamEmailClassifier\\spamDataset", "D:\\projects\\spamEmailClassifier\\nonspamDataset")
# trainingSpamTokenList, testSpamTokenList, trainingNonSpamTokenList, testNonSpamTokenList = getNormalizedEmailList(trainingSetSpamFileList, testSetSpamFileList, trainingSetNonSpamFileList, testSetNonSpamFileList)
# print trainingSpamTokenList, testSpamTokenList, trainingNonSpamTokenList, testNonSpamTokenList
