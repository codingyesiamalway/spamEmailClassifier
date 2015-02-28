__author__ = 'Yu Zhao'
from os import listdir
from os.path import isfile, join
import re


def createEmailList(spamFile, nonSpamFile):
    spamEmailList = []
    with open(spamFile, 'r') as file :
        curEmail = ''
        for curLine in file:
            line = curLine.strip()
            if line == '----':
                if curEmail != "":
                    spamEmailList = spamEmailList + [curEmail]
                curEmail = ''
            elif curEmail != "":
                curEmail = curEmail + ' ' + line
            else:
                curEmail = line

    return spamEmailList

def getSpamDataSet(directory):
    spamEmailList = []
    onlyfiles = [ f for f in listdir(directory) if isfile(join(directory,f)) ]
    for i in onlyfiles:
        with open(directory + "/" + i, 'r') as file :
            data=file.read().replace('\n', '').replace('1', ' one ').replace('2', ' two ').replace('3', ' three ').replace('4', ' four ').replace('5', ' five ').replace('6', ' six ').replace('7', ' seven ').replace('8', ' eight ').replace('9', ' nine ').replace('0', ' zero ')
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
    return dict


x = getSpamDataSet("spamDataset")
y = getTokenCountFromTokenList(x)
z = sorted(y, key=y.get,  reverse=True)
print z

#x = createEmailList("spam.txt", '')
#print x